import re
from xml.sax.saxutils import escape

from bpkio_api.exceptions import BroadpeakIoHelperError
from bpkio_cli.core.exceptions import UnexpectedContentError
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.formatter import OutputFormatter
from lxml import etree
from media_muncher.handlers import DASHHandler


class XMLFormatter(OutputFormatter):
    def __init__(self, handler: DASHHandler) -> None:
        super().__init__()
        self.handler = handler

    def format(self, mode="standard", top: int = 0, tail: int = 0, **kwargs):
        try:
            match mode:
                case "raw":
                    output = self.raw()
                case "standard":
                    output = self.pretty_print(
                        root=self.handler.xml_document,
                        uri_attributes=self.handler.uri_attributes,
                        uri_elements=self.handler.uri_elements,
                        **kwargs,
                    )

            output = self.trim(output, top, tail)
            return output

        except BroadpeakIoHelperError as e:
            out = self.handler.content.decode()
            out += "\n\n"
            out += CL.error(f"Error - {e.message}: {e.original_message}")
            return out

        except Exception as e:
            raise UnexpectedContentError(
                message="Error formatting the content. "
                "It does not appear to be a valid MPD document. {}\n"
                "Raw content: \n{}".format(e, self.handler.content)
            )

    def raw(self):
        # Pretty-print the XML using the ElementTree's tostring() method
        # return etree.tostring(self.handler.xml_document, pretty_print=True)

        return self.handler.content.decode()

    @staticmethod
    def pretty_print(
        root,
        namespaces={},
        uri_elements=[],
        uri_attributes=[],
        ad_pattern=None,
        **kwargs,
    ):
        """Pretty-print the XML with colored output

        Returns:
            str
        """
        # TODO - Fix. The closing tags are added twice for nodes with text content

        # Get the namespaces in the root element
        namespaces.update(root.nsmap)

        ns_mappings = dict((v, k + ":" if k else "") for k, v in namespaces.items())

        indent = CL.markup("\u2502  ")

        # Recursively pretty-print the XML with colored output and return as a string
        def _pretty_print(node, level=0, position=0):
            result = indent * level

            if isinstance(node, etree._Comment):
                result = result + CL.markup(node) + "\n"
                return result

            tag = node.tag
            # Resolve namespaces:
            if "{" in tag:
                tag = re.sub(
                    r"{(.*)}",
                    lambda m: ns_mappings.get(m.group(1), m.group(0)),
                    tag,
                )
            resolved_tag = tag

            # Add a line if there are multiple periods
            if resolved_tag == "Period" and position > 0:
                result += (
                    CL.make_separator(length=150, mode="xml") + "\n" + indent * level
                )

            # Start the opening tag
            result = result + "<"

            # Color-code the element tag name
            tag = CL.node(tag)

            # Add the namespaces
            if level == 0:
                ns_strings = []
                for k, v in namespaces.items():
                    if k:
                        ns_string = f'xmlns:{k}="{v}"'
                    else:
                        ns_string = f'xmlns="{v}"'

                    ns_string = CL.attr(ns_string)
                    ns_strings.append(ns_string)
                n_str = " " + " ".join(ns_strings)
                tag += n_str

            # Add the namespace to the tag name, if necessary
            # if node.prefix:
            # tag = f"{Fore.YELLOW}{node.prefix}:{Fore.GREEN}{tag}"

            # Color-code the attributes
            if node.attrib:
                attr_strings = []
                for k, v in node.attrib.items():
                    # Replace namespace with prefix
                    if "{" in k:
                        k = re.sub(
                            r"{(.*)}",
                            lambda m: ns_mappings.get(m.group(1), m.group(0)),
                            k,
                        )

                    attr_value = escape(v, {'"': "&quot;"})

                    key_colored = CL.attr(k)
                    if k.startswith("bic:"):
                        key_colored = CL.bic_label("bic:") + CL.orange(k[4:])

                    value_colored = CL.value(attr_value)
                    if k in uri_attributes:
                        value_colored = CL.url(attr_value)
                    if k.startswith("bic:"):
                        value_colored = CL.comment(attr_value)

                    attr_string = '{key}="{value}"'.format(
                        key=key_colored,
                        value=value_colored,
                    )
                    attr_strings.append(attr_string)
                attr_str = " " + " ".join(attr_strings)
                tag += attr_str

            # Add the tag
            result += tag

            # Close the tag
            pure_text = node.text.strip() if node.text else ""
            if not pure_text and not len(pure_text) and not len(node):
                result += "/>"
                return result + "\n"
            else:
                result += ">"

            # Add the text content, if any
            if node.text and node.text.strip():
                text = node.text.strip()
                if resolved_tag in uri_elements:
                    if ad_pattern and ad_pattern in text:
                        if "/slate_" in text:
                            text = CL.url_slate(text)
                        else:
                            text = CL.url_ad(text)
                    else:
                        text = CL.url(text)
                result += text

            # Recurse into child nodes
            if len(node):
                result += "\n"
                for i, child in enumerate(node):
                    result += _pretty_print(child, level + 1, position=i)

            # Add the closing tag
            if len(node):
                result += indent * level

            result += f"</{CL.node(resolved_tag)}>\n"

            return result

        # Pretty-print the XML with colored output and include the XML declaration
        declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_string = _pretty_print(root)
        valid_xml = f"{declaration}{xml_string}\n"

        return valid_xml
