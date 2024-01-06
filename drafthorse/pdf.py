# Based on code of the factur-x Python package:
# Copyright 2016-2018, Alexis de Lattre <alexis.delattre@akretion.com>
# Modified for ZUGFeRD and Python 3 by Raphael Michel, 2018
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * The name of the authors may not be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import logging
from datetime import datetime
from io import BytesIO
from lxml import etree
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
    create_string_object,
)

from drafthorse.xmp_schema import XMP_SCHEMA

logging.basicConfig()
logger = logging.getLogger("drafthorse")
logger.setLevel(logging.INFO)


def attach_xml(original_pdf, xml_data):
    """
    Create the ZUGFeRD invoice by attaching
    the input XML and proper metadata
    :param original_pdf: Input PDF
    :param xml_data: Input XML
    :return: Output PDF containing the metadata and XML
    """
    if not isinstance(original_pdf, bytes):
        raise TypeError("Please supply original PDF as bytes.")
    if not isinstance(xml_data, bytes):
        raise TypeError("Please supply XML data as bytes.")

    reader = PdfReader(BytesIO(original_pdf))
    output = PdfWriter()

    output._header = "%PDF-1.6\r\n%\xc7\xec\x8f\xa2".encode()
    output.append_pages_from_reader(reader)

    original_pdf_id = reader.trailer.get("/ID")
    if original_pdf_id:
        output._ID = original_pdf_id
        # else : generate some ?

    # Extract metadata from XML
    pdf_metadata, profile = _extract_xml_info(xml_data)

    # Extract output intents from input PDF
    output_intents = _get_original_output_intents(reader)

    _update_metadata_add_attachment(
        output, xml_data, pdf_metadata, profile, output_intents
    )

    outbuffer = BytesIO()
    output.write(outbuffer)
    outbuffer.seek(0)
    return outbuffer.read()


def _get_original_output_intents(original_pdf):
    """
    Get output intents from input PDF
    :param original_pdf: Input PDF
    :return: Output PDF metadata information
    """
    output_intents = []
    try:
        pdf_root = original_pdf.trailer["/Root"]
        ori_output_intents = pdf_root["/OutputIntents"]
        for ori_output_intent in ori_output_intents:
            ori_output_intent_dict = ori_output_intent.get_object()
            dest_output_profile_dict = ori_output_intent_dict[
                "/DestOutputProfile"
            ].get_object()
            output_intents.append((ori_output_intent_dict, dest_output_profile_dict))
    except Exception as ex:
        logger.error(ex)
    return output_intents


def _prepare_pdf_metadata_txt(pdf_metadata):
    """
    Create PDF info for the Document Properties section
    :param pdf_metadata: Metadata
    :return: PDF info
    """
    pdf_date = datetime.utcnow().strftime("D:%Y%m%d%H%M%SZ")
    info_dict = {
        "/Author": pdf_metadata.get("author", ""),
        "/CreationDate": pdf_date,
        "/Creator": "python-drafthorse",
        "/Keywords": pdf_metadata.get("keywords", ""),
        "/ModDate": pdf_date,
        "/Subject": pdf_metadata.get("subject", ""),
        "/Title": pdf_metadata.get("title", ""),
    }
    return info_dict


def _prepare_xmp_metadata(profile, pdf_metadata):
    """
    Prepare pdf metadata using the FACTUR-X XMP extension schema
    :param profile: Invoice profile
    :param pdf_metadata: PDF metadata
    :return: metadata XML
    """
    xml_str = XMP_SCHEMA.format(
        title=pdf_metadata.get("title", ""),
        author=pdf_metadata.get("author", ""),
        subject=pdf_metadata.get("subject", ""),
        producer="pypdf",
        creator_tool="python-drafthorse",
        timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        urn="urn:factur-x:pdfa:CrossIndustryDocument:invoice:1p0#",
        documenttype="INVOICE",
        xml_filename="factur-x.xml",
        version="1.0",
        xmp_level=profile,
    )
    xml_byte = xml_str.encode("utf-8")

    return xml_byte


def _update_metadata_add_attachment(
    pdf_filestream, facturx_xml_str, pdf_metadata, facturx_level, output_intents
):
    """
    Update PDF metadata and attach XML file
    :param pdf_filestream: PDF data
    :param facturx_xml_str: XML data
    :param pdf_metadata: PDF metadata
    :param facturx_level: Invoice profile
    :param output_intents: Output intents from input PDF
    """
    # Disable encoding
    # md5sum = hashlib.md5(facturx_xml_str).hexdigest()
    # md5sum_obj = create_string_object(md5sum)
    pdf_date = datetime.utcnow().strftime("D:%Y%m%d%H%M%SZ")
    params_dict = DictionaryObject(
        {
            # NameObject('/CheckSum'): md5sum_obj,
            NameObject("/ModDate"): create_string_object(pdf_date),
            NameObject("/CreationDate"): create_string_object(pdf_date),
            NameObject("/Size"): create_string_object(str(len(facturx_xml_str))),
        }
    )
    file_entry = DecodedStreamObject()
    file_entry.set_data(facturx_xml_str)
    file_entry.update(
        {
            NameObject("/Type"): NameObject("/EmbeddedFile"),
            NameObject("/Params"): params_dict,
            # 2F is '/' in hexadecimal
            NameObject("/Subtype"): NameObject("/text#2Fxml"),
        }
    )
    file_entry_obj = pdf_filestream._add_object(file_entry)
    # The Filespec entry
    ef_dict = DictionaryObject(
        {NameObject("/F"): file_entry_obj, NameObject("/UF"): file_entry_obj}
    )

    fname_obj = create_string_object("factur-x.xml")
    filespec_dict = DictionaryObject(
        {
            NameObject("/AFRelationship"): NameObject(
                "/Data" if facturx_level in ("BASIC-WL", "MINIMUM") else "/Alternative"
            ),
            NameObject("/Desc"): create_string_object(
                "Invoice metadata conforming to ZUGFeRD standard (http://www.ferd-net.de/)"
            ),
            NameObject("/Type"): NameObject("/Filespec"),
            NameObject("/F"): fname_obj,
            NameObject("/EF"): ef_dict,
            NameObject("/UF"): fname_obj,
        }
    )
    filespec_obj = pdf_filestream._add_object(filespec_dict)
    name_arrayobj_cdict = {fname_obj: filespec_obj}
    name_arrayobj_content_sort = list(
        sorted(name_arrayobj_cdict.items(), key=lambda x: x[0])
    )
    name_arrayobj_content_final = []
    af_list = []
    for fname_obj, filespec_obj in name_arrayobj_content_sort:
        name_arrayobj_content_final += [fname_obj, filespec_obj]
        af_list.append(filespec_obj)
    embedded_files_names_dict = DictionaryObject(
        {NameObject("/Names"): ArrayObject(name_arrayobj_content_final)}
    )
    # Then create the entry for the root, as it needs a
    # reference to the Filespec
    embedded_files_dict = DictionaryObject(
        {NameObject("/EmbeddedFiles"): embedded_files_names_dict}
    )
    res_output_intents = []
    for output_intent_dict, dest_output_profile_dict in output_intents:
        dest_output_profile_obj = pdf_filestream._add_object(dest_output_profile_dict)
        # TODO detect if there are no other objects in output_intent_dest_obj
        # than /DestOutputProfile
        output_intent_dict.update(
            {NameObject("/DestOutputProfile"): dest_output_profile_obj}
        )
        output_intent_obj = pdf_filestream._add_object(output_intent_dict)
        res_output_intents.append(output_intent_obj)
    # Update the root
    metadata_xml_str = _prepare_xmp_metadata(facturx_level, pdf_metadata)
    metadata_file_entry = DecodedStreamObject()
    metadata_file_entry.set_data(metadata_xml_str)
    metadata_file_entry.update(
        {
            NameObject("/Subtype"): NameObject("/XML"),
            NameObject("/Type"): NameObject("/Metadata"),
        }
    )
    metadata_obj = pdf_filestream._add_object(metadata_file_entry)
    af_value_obj = pdf_filestream._add_object(ArrayObject(af_list))
    pdf_filestream._root_object.update(
        {
            NameObject("/AF"): af_value_obj,
            NameObject("/Metadata"): metadata_obj,
            NameObject("/Names"): embedded_files_dict,
            # show attachments when opening PDF
            NameObject("/PageMode"): NameObject("/UseAttachments"),
        }
    )
    if res_output_intents:
        pdf_filestream._root_object.update(
            {NameObject("/OutputIntents"): ArrayObject(res_output_intents)}
        )
    metadata_txt_dict = _prepare_pdf_metadata_txt(pdf_metadata)
    pdf_filestream.add_metadata(metadata_txt_dict)


def _extract_xml_info(xml_data):
    """
    Extract metadata and profile from XML further added to the PDF
    :param xml_data: XML data
    :return: Metadata and profile
    """
    INVOICE_TYPE_CODE = "380"

    xml_etree = etree.fromstring(xml_data)
    namespaces = xml_etree.nsmap

    # get metadata
    date_xpath = xml_etree.xpath(
        "//rsm:ExchangedDocument/ram:IssueDateTime/udt:DateTimeString",
        namespaces=namespaces,
    )
    date = date_xpath[0].text
    date_format = date_xpath[0].attrib and date_xpath[0].attrib.get("format") or "102"
    format_map = {
        "102": "%Y%m%d",
        "203": "%Y%m%d%H%M",
    }
    date_dt = datetime.strptime(date, format_map.get(date_format, format_map["102"]))
    number_xpath = xml_etree.xpath(
        "//rsm:ExchangedDocument/ram:ID", namespaces=namespaces
    )
    number = number_xpath[0].text
    seller_xpath = xml_etree.xpath(
        "//ram:ApplicableHeaderTradeAgreement/ram:SellerTradeParty/ram:Name",
        namespaces=namespaces,
    )
    seller = seller_xpath[0].text

    doc_type_xpath = xml_etree.xpath(
        "//rsm:ExchangedDocument/ram:TypeCode", namespaces=namespaces
    )
    doc_type = doc_type_xpath[0].text
    if doc_type != INVOICE_TYPE_CODE:
        raise Exception(
            "Invalid doc type! XML value for TypeCode shall be 380 for an invoice."
        )

    doc_type_name = "Invoice"
    date_str = datetime.strftime(date_dt, "%Y-%m-%d")
    pdf_metadata = {
        "author": seller,
        "keywords": "{}, {}".format(doc_type_name, "Factur-X"),
        "title": "{}: {} {}".format(seller, doc_type_name, number),
        "subject": "{} {} dated {} issued by {}".format(
            doc_type_name, number, date_str, seller
        ),
    }

    # get profile
    doc_id_xpath = xml_etree.xpath(
        "//rsm:ExchangedDocumentContext"
        "/ram:GuidelineSpecifiedDocumentContextParameter"
        "/ram:ID",
        namespaces=namespaces,
    )
    doc_id = doc_id_xpath[0].text

    profile = doc_id.split(":")[-1]
    if doc_id.split(":")[-1] in ["basic", "extended"]:
        profile = doc_id.split(":")[-1]
    elif doc_id.split(":")[-2] == "en16931":
        profile = doc_id.split(":")[-2]
        profile = profile[:2] + " " + profile[2:]
    else:
        raise Exception("Invalid XML profile!")

    profile = profile.upper()
    logger.info(f"Invoide profile dectected from XML: {profile}")

    return pdf_metadata, profile
