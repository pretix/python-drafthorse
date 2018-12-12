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
import datetime
import hashlib
import os
from io import BytesIO

from lxml import etree
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import (ArrayObject, DecodedStreamObject, DictionaryObject,
                            NameObject, createStringObject)


def attach_xml(original_pdf, xml_data, level='BASIC'):
    if not isinstance(original_pdf, bytes):
        raise TypeError("Please supply original PDF as bytes.")
    if not isinstance(xml_data, bytes):
        raise TypeError("Please supply XML data as bytes.")

    reader = PdfFileReader(BytesIO(original_pdf))
    output = PdfFileWriter()
    # for page in reader.pages:
    #    output.addPage(page)

    output._header = "%PDF-1.6\r\n%\xc7\xec\x8f\xa2".encode()
    output.appendPagesFromReader(reader)

    original_pdf_id = reader.trailer.get('/ID')
    if original_pdf_id:
        output._ID = original_pdf_id
        # else : generate some ?

    _facturx_update_metadata_add_attachment(
        output, xml_data, {}, level,
        output_intents=_get_original_output_intents(reader),
    )

    outbuffer = BytesIO()
    output.write(outbuffer)
    outbuffer.seek(0)
    return outbuffer.read()


def _get_original_output_intents(original_pdf):
    output_intents = []
    try:
        pdf_root = original_pdf.trailer['/Root']
        ori_output_intents = pdf_root['/OutputIntents']
        for ori_output_intent in ori_output_intents:
            ori_output_intent_dict = ori_output_intent.getObject()
            dest_output_profile_dict = \
                ori_output_intent_dict['/DestOutputProfile'].getObject()
            output_intents.append(
                (ori_output_intent_dict, dest_output_profile_dict))
    except:  # noqa
        pass
    return output_intents


def _prepare_pdf_metadata_txt(pdf_metadata):
    pdf_date = datetime.datetime.utcnow().strftime('D:%Y%m%d%H%M%SZ')
    info_dict = {
        '/Author': pdf_metadata.get('author', ''),
        '/CreationDate': pdf_date,
        '/Creator': 'python-drafthorse',
        '/Keywords': pdf_metadata.get('keywords', ''),
        '/ModDate': pdf_date,
        '/Subject': pdf_metadata.get('subject', ''),
        '/Title': pdf_metadata.get('title', ''),
    }
    return info_dict


def _prepare_pdf_metadata_xml(level, pdf_metadata):
    nsmap_x = {'x': 'adobe:ns:meta/'}
    nsmap_rdf = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}
    nsmap_dc = {'dc': 'http://purl.org/dc/elements/1.1/'}
    nsmap_pdf = {'pdf': 'http://ns.adobe.com/pdf/1.3/'}
    nsmap_xmp = {'xmp': 'http://ns.adobe.com/xap/1.0/'}
    nsmap_pdfaid = {'pdfaid': 'http://www.aiim.org/pdfa/ns/id/'}
    nsmap_zf = {'zf': 'urn:ferd:pdfa:CrossIndustryDocument:invoice:1p0#'}
    ns_x = '{%s}' % nsmap_x['x']
    ns_dc = '{%s}' % nsmap_dc['dc']
    ns_rdf = '{%s}' % nsmap_rdf['rdf']
    ns_pdf = '{%s}' % nsmap_pdf['pdf']
    ns_xmp = '{%s}' % nsmap_xmp['xmp']
    ns_pdfaid = '{%s}' % nsmap_pdfaid['pdfaid']
    ns_zf = '{%s}' % nsmap_zf['zf']
    ns_xml = '{http://www.w3.org/XML/1998/namespace}'

    root = etree.Element(ns_x + 'xmpmeta', nsmap=nsmap_x)
    rdf = etree.SubElement(root, ns_rdf + 'RDF', nsmap=nsmap_rdf)
    desc_pdfaid = etree.SubElement(rdf, ns_rdf + 'Description', nsmap=nsmap_pdfaid)
    desc_pdfaid.set(ns_rdf + 'about', '')
    etree.SubElement(desc_pdfaid, ns_pdfaid + 'part').text = '3'
    etree.SubElement(desc_pdfaid, ns_pdfaid + 'conformance').text = 'B'
    desc_dc = etree.SubElement(rdf, ns_rdf + 'Description', nsmap=nsmap_dc)
    desc_dc.set(ns_rdf + 'about', '')
    dc_title = etree.SubElement(desc_dc, ns_dc + 'title')
    dc_title_alt = etree.SubElement(dc_title, ns_rdf + 'Alt')
    dc_title_alt_li = etree.SubElement(dc_title_alt, ns_rdf + 'li')
    dc_title_alt_li.text = pdf_metadata.get('title', '')
    dc_title_alt_li.set(ns_xml + 'lang', 'x-default')
    dc_creator = etree.SubElement(desc_dc, ns_dc + 'creator')
    dc_creator_seq = etree.SubElement(dc_creator, ns_rdf + 'Seq')
    etree.SubElement(dc_creator_seq, ns_rdf + 'li').text = pdf_metadata.get('author', '')
    dc_desc = etree.SubElement(desc_dc, ns_dc + 'description')
    dc_desc_alt = etree.SubElement(dc_desc, ns_rdf + 'Alt')
    dc_desc_alt_li = etree.SubElement(dc_desc_alt, ns_rdf + 'li')
    dc_desc_alt_li.text = pdf_metadata.get('subject', '')
    dc_desc_alt_li.set(ns_xml + 'lang', 'x-default')
    desc_adobe = etree.SubElement(rdf, ns_rdf + 'Description', nsmap=nsmap_pdf)
    desc_adobe.set(ns_rdf + 'about', '')
    producer = etree.SubElement(desc_adobe, ns_pdf + 'Producer')
    producer.text = 'PyPDF2'
    desc_xmp = etree.SubElement(rdf, ns_rdf + 'Description', nsmap=nsmap_xmp)
    desc_xmp.set(ns_rdf + 'about', '')
    creator = etree.SubElement(desc_xmp, ns_xmp + 'CreatorTool')
    creator.text = 'python-drafthorse'
    xmp_date = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + '+00:00'
    etree.SubElement(desc_xmp, ns_xmp + 'CreateDate').text = xmp_date
    etree.SubElement(desc_xmp, ns_xmp + 'ModifyDate').text = xmp_date

    # Now is the ZUGFeRD description tag
    zugferd_desc = etree.SubElement(rdf, ns_rdf + 'Description', nsmap=nsmap_zf)
    zugferd_desc.set(ns_rdf + 'about', '')
    fx_doc_type = etree.SubElement(zugferd_desc, ns_zf + 'DocumentType', nsmap=nsmap_zf)
    fx_doc_type.text = 'INVOICE'
    fx_doc_filename = etree.SubElement(zugferd_desc, ns_zf + 'DocumentFileName', nsmap=nsmap_zf)
    fx_doc_filename.text = 'ZUGFeRD-invoice.xml'
    fx_doc_version = etree.SubElement(zugferd_desc, ns_zf + 'Version', nsmap=nsmap_zf)
    fx_doc_version.text = '1.0'
    fx_conformance_level = etree.SubElement(zugferd_desc, ns_zf + 'ConformanceLevel', nsmap=nsmap_zf)
    fx_conformance_level.text = level

    xmp_file = os.path.join(os.path.dirname(__file__), 'schema', 'ZUGFeRD1p0_extension_schema.xmp')
    # Reason for defining a parser below:
    # http://lxml.de/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output
    parser = etree.XMLParser(remove_blank_text=True)
    facturx_ext_schema_root = etree.parse(open(xmp_file), parser)
    # The Factur-X extension schema must be embedded into each PDF document
    facturx_ext_schema_desc_xpath = facturx_ext_schema_root.xpath('//rdf:Description', namespaces=nsmap_rdf)
    rdf.append(facturx_ext_schema_desc_xpath[1])

    # TODO: should be UTF-16be ??
    xml_str = etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=False)
    head = u'<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>'.encode('utf-8')
    tail = u'<?xpacket end="w"?>'.encode('utf-8')
    xml_final_str = head + xml_str + tail
    return xml_final_str


def _facturx_update_metadata_add_attachment(pdf_filestream, facturx_xml_str, pdf_metadata, facturx_level,
                                            output_intents):
    md5sum = hashlib.md5(facturx_xml_str).hexdigest()
    md5sum_obj = createStringObject(md5sum)
    pdf_date = datetime.datetime.utcnow().strftime('D:%Y%m%d%H%M%SZ')
    params_dict = DictionaryObject({
        #NameObject('/CheckSum'): md5sum_obj,
        NameObject('/ModDate'): createStringObject(pdf_date),
        NameObject('/CreationDate'): createStringObject(pdf_date),
        NameObject('/Size'): NameObject(str(len(facturx_xml_str))),
    })
    file_entry = DecodedStreamObject()
    file_entry.setData(facturx_xml_str)  # here we integrate the file itself
    file_entry.update({
        NameObject("/Type"): NameObject("/EmbeddedFile"),
        NameObject("/Params"): params_dict,
        # 2F is '/' in hexadecimal
        NameObject("/Subtype"): NameObject("/text#2Fxml"),
    })
    file_entry_obj = pdf_filestream._addObject(file_entry)
    # The Filespec entry
    ef_dict = DictionaryObject({
        NameObject("/F"): file_entry_obj,
        NameObject('/UF'): file_entry_obj,
    })

    fname_obj = createStringObject("ZUGFeRD-invoice.xml")
    filespec_dict = DictionaryObject({
        NameObject("/AFRelationship"): NameObject("/Alternative"),
        NameObject("/Desc"): createStringObject("Invoice metadata conforming to ZUGFeRD standard (http://www.ferd-net.de/front_content.php?idcat=231&lang=4)"),
        NameObject("/Type"): NameObject("/Filespec"),
        NameObject("/F"): fname_obj,
        NameObject("/EF"): ef_dict,
        NameObject("/UF"): fname_obj,
    })
    filespec_obj = pdf_filestream._addObject(filespec_dict)
    name_arrayobj_cdict = {fname_obj: filespec_obj}
    name_arrayobj_content_sort = list(
        sorted(name_arrayobj_cdict.items(), key=lambda x: x[0]))
    name_arrayobj_content_final = []
    af_list = []
    for (fname_obj, filespec_obj) in name_arrayobj_content_sort:
        name_arrayobj_content_final += [fname_obj, filespec_obj]
        af_list.append(filespec_obj)
    embedded_files_names_dict = DictionaryObject({
        NameObject("/Names"): ArrayObject(name_arrayobj_content_final),
    })
    # Then create the entry for the root, as it needs a
    # reference to the Filespec
    embedded_files_dict = DictionaryObject({
        NameObject("/EmbeddedFiles"): embedded_files_names_dict,
    })
    res_output_intents = []
    for output_intent_dict, dest_output_profile_dict in output_intents:
        dest_output_profile_obj = pdf_filestream._addObject(
            dest_output_profile_dict)
        # TODO detect if there are no other objects in output_intent_dest_obj
        # than /DestOutputProfile
        output_intent_dict.update({
            NameObject("/DestOutputProfile"): dest_output_profile_obj,
        })
        output_intent_obj = pdf_filestream._addObject(output_intent_dict)
        res_output_intents.append(output_intent_obj)
    # Update the root
    metadata_xml_str = _prepare_pdf_metadata_xml(facturx_level, pdf_metadata)
    metadata_file_entry = DecodedStreamObject()
    metadata_file_entry.setData(metadata_xml_str)
    metadata_file_entry.update({
        NameObject('/Subtype'): NameObject('/XML'),
        NameObject('/Type'): NameObject('/Metadata'),
    })
    metadata_obj = pdf_filestream._addObject(metadata_file_entry)
    af_value_obj = pdf_filestream._addObject(ArrayObject(af_list))
    pdf_filestream._root_object.update({
        NameObject("/AF"): af_value_obj,
        NameObject("/Metadata"): metadata_obj,
        NameObject("/Names"): embedded_files_dict,
        # show attachments when opening PDF
        NameObject("/PageMode"): NameObject("/UseAttachments"),
    })
    if res_output_intents:
        pdf_filestream._root_object.update({
            NameObject("/OutputIntents"): ArrayObject(res_output_intents),
        })
    metadata_txt_dict = _prepare_pdf_metadata_txt(pdf_metadata)
    pdf_filestream.addMetadata(metadata_txt_dict)
