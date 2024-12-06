# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 12:53:07 2024

@author: cvskf
"""

import os
from lxml import etree
import json


class All(etree.ElementBase):
    ""
    
    @property
    def parse(self):
        ""
        l = []
        
        for e in self:
            
            if e.tag == '{http://www.w3.org/2001/XMLSchema}element':
                
                l.append(e.parse)
            
            else:
                
                raise Exception(e.tag)
        
        return l


class Annotation(etree.ElementBase):
    ""
    
    @property
    def documentation(self):
        ""
        return self.find('{http://www.w3.org/2001/XMLSchema}documentation')
    
    @property
    def has_documentation(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}documentation')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def parse(self):
        ""
        #print('self.has_documentation', self.has_documentation)
        if self.has_documentation:
            return self.documentation.parse
        else:
            return ''
    
        


class Attribute(etree.ElementBase):
    ""
    
    
class Choice(etree.ElementBase):
    ""
    
    @property
    def parse(self):
        ""
        l = []
        
        for e in self:
            
            if e.tag == '{http://www.w3.org/2001/XMLSchema}element':
                
                l.append(e.parse)
            
            else:
                
                raise Exception(e.tag)
        
        return l
    
    
    
class ComplexType(etree.ElementBase):
    ""
    @property
    def annotation(self):
        ""
        return self.find('{http://www.w3.org/2001/XMLSchema}annotation')
    
    @property
    def documentation(self):
        ""
        return self.annotation.documentation
    
    @property
    def has_annotation(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}annotation')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def has_associated_element(self):
        ""
        x = self.getparent().find((f'{{http://www.w3.org/2001/XMLSchema}}element[@type="{self.name}"]'))
        if not x is None:
            return True
        else:
            return False
        
    @property
    def has_documentation(self):
        ""
        if self.has_annotation:
            return self.annotation.has_documentation
        else:
            return False
        
    @property
    def has_simple_content(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}simpleContent')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def name(self):
        ""
        return self.attrib.get('name')
        
    @property
    def parse(self):
        ""
        #result = ''
        
        d = dict(
            documentation = self.documentation.parse if self.has_documentation else None,
            subclasses = []
            )
                
        for e in self:
            
            if e.tag == '{http://www.w3.org/2001/XMLSchema}annotation':
                
                pass
                    
            elif e.tag == '{http://www.w3.org/2001/XMLSchema}all':
                
                d['subclasses'].extend(e.parse)
            
            elif e.tag == '{http://www.w3.org/2001/XMLSchema}sequence':
                
                d['subclasses'].extend(e.parse)
            
            elif e.tag == '{http://www.w3.org/2001/XMLSchema}choice':
                
                d['subclasses'].extend(e.parse)
            
            elif e.tag == '{http://www.w3.org/2001/XMLSchema}simpleContent':
                
                pass
                
            else:
                
                raise Exception(e.tag)
                
            #break
    
        return d
    
    @property
    def parse_annotation(self):
        ""
        #print('self.has_annotation', self.has_annotation)
        if self.has_annotation:
            #print('self.annotation.parse', self.annotation.parse)
            return self.annotation.parse
        else:
            return ''
        
    @property
    def simple_content(self):
        ""
        return self.find('{http://www.w3.org/2001/XMLSchema}simpleContent')
    
    

class Documentation(etree.ElementBase):
    ""
    
    @property
    def parse(self):
        ""
        x = self.text.replace('\n', ' ').replace('²','2').replace('–', '-').replace('’', "'").replace('°','deg')
        if x.endswith('"'):
            x += '.'
        x = ' '.join(x.split())
        return x
   
    
    
class Element(etree.ElementBase):
    ""
    
    @property
    def annotation(self):
        ""
        return self.find('{http://www.w3.org/2001/XMLSchema}annotation')
        
    @property
    def class_name(self):
        ""
        return self.name.replace('-','_')
        
    @property
    def complex_type(self):
        ""
        if self.has_complex_type_child:
            return self.find('{http://www.w3.org/2001/XMLSchema}complexType')
        else:
            
            type_name = self.type_name
            # fix
            if self.name == 'Storage-Heater':
                type_name = 'Storage-Heater' 
            elif self.name == 'Storage-Heaters':
                type_name = 'Storage-Heaters' 
                
            
            for schemaLocation, root in schema_roots.items():
                x = root.find((f'{{http://www.w3.org/2001/XMLSchema}}complexType[@name="{type_name}"]'))
                if not x is None:
                    return x
                
        return None 
    
    @property
    def complex_type_location(self):
        ""
        if self.has_complex_type_child:
            return None
        else:
            
            type_name = self.type_name
            # fix
            if self.name == 'Storage-Heater':
                type_name = 'Storage-Heater' 
            elif self.name == 'Storage-Heaters':
                type_name = 'Storage-Heaters' 
                
            
            for schemaLocation, root in schema_roots.items():
                x = root.find((f'{{http://www.w3.org/2001/XMLSchema}}complexType[@name="{type_name}"]'))
                if not x is None:
                    return schemaLocation
                
        return None 
    
    @property
    def documentation(self):
        ""
        return self.annotation.documentation
        
    @property
    def has_annotation(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}annotation')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def has_documentation(self):
        ""
        if self.has_annotation:
            return self.annotation.has_documentation
        else:
            return False
        
        
    @property
    def has_complex_type_child(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}complexType')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def has_simple_content(self):
        ""
        if self.is_complex_type:
            return self.complex_type.has_simple_content
        else:
            return False
        
    @property
    def has_simple_type_child(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}simpleType')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def has_text_node(self):
        ""
        if (self.is_xs_type 
            or self.is_simple_type 
            or (self.is_complex_type and self.complex_type.has_simple_content)
            ):
            return True
        else:
            return False
        
    @property
    def has_type_name(self):
        ""
        x = self.attrib.get('type')
        if not x is None:
            return True
        else:
            return False
       
    @property
    def is_complex_type(self):
        ""
        if not self.complex_type is None:
            return True
        else:
            return False
        
    @property
    def is_multiple(self):
        ""
        if self.max_occurs == 'unbounded':
            return True
        elif self.max_occurs > 1:
            return True
        else:
            return False
    
    @property
    def is_optional(self):
        ""
        if self.min_occurs == 0:
            return True
        else:
            return False
        
    @property
    def is_simple_type(self):
        ""
        if not self.simple_type is None:
            return True
        else:
            return False
        
    @property
    def is_xs_type(self):
        ""
        if self.has_type_name:
            if self.type_name.startswith('xs:'):
                return True
            else:
                return False
        return False
    
    @property
    def name(self):
        ""
        return self.attrib.get('name')
    
    @property
    def map_codes(self):
        ""
        if self.is_simple_type:
            return self.simple_type.map_codes
        elif self.has_simple_content:
            return self.complex_type.simple_content.map_codes
        elif self.is_xs_type:
            if self.xs_type == 'boolean':
                return {'true': True, '1': True, 'false': False, '0': False}
            else:
                return None
        else:
            return None
            
    @property
    def map_values(self): 
        ""
        if self.map_codes is None:
            return None
        else:
            return {v:k for k,v in self.map_codes.items()}
    
    @property
    def max_occurs(self):
        ""
        x = self.attrib.get('maxOccurs',1)
        if x == 'unbounded':
            return x
        else:
            return (int(x))
        
    @property
    def method_name(self):
        ""
        method_name = self.class_name.lower()
        if method_name == 'property':
            method_name += '_'
        return method_name
    
    @property
    def min_occurs(self):
        ""
        return int(self.attrib.get('minOccurs',1))
    
    
    @property
    def parse(self):
        ""
        
        print('  -', self.name, '(Element.parse)')
        
        
        d = dict(
            name = self.name,
            class_name = self.class_name,
            type = self.attrib.get('type'),
            documentation = self.documentation.parse if self.has_documentation else None,
            has_text_node = self.has_text_node,
            min_occurs = self.min_occurs,
            max_occurs = self.max_occurs,
            python_type_convertor = self.python_type_convertor if self.has_text_node else None,
            map_codes = self.map_codes,
            map_values = self.map_values
            )
        
        if self.is_complex_type:
            d.update(subclass_dict = self.complex_type.parse)
        else:
            d.update(subclass_dict = dict(documentation = None, subclasses = []))
        
        
        return d
        
        
        
        
        # result = ''
        # result += f'class {self.class_name}(_Base, etree.ElementBase):\n'
        # result += '    ""'
        # result += '\n'
        
        
        
        # if self.is_complex_type:
            
        #     x = self.complex_type.parse
        #     result += '    ' + '\n    '.join(x.split('\n'))
            
            
        # elif self.is_simple_type:
            
        #     if self.has_documentation:
        #         result += f'    documentation = """{self.documentation.parse}"""\n'
            
        #     x = self.simple_type.parse
        #     result += '    ' + '\n    '.join(x.split('\n'))
            
        # elif self.is_xs_type:
            
        #     if self.has_documentation:
        #         result += f'    documentation = """{self.documentation.parse}"""\n'
                
        #     result += f'    xs_type = "{self.xs_type}"\n'
        #     result += f'    python_type = {self.python_type_convertor}\n'
            
        #     if self.xs_type == 'boolean':
        #         map_dict = {'true': True, '1': True, 'false': False, '0': False}
        #     else:
        #         map_dict = {}
        #     result += f'    map_codes = {str(map_dict)}\n'
        #     map_dict2 = {v:k for k,v in map_dict.items()}
        #     result += f'    map_values = {str(map_dict2)}\n'
            
        #     result += '\n'
        #     result += '    @property\n'
        #     result += '    def value(self): return self.__class__.map_codes[self.text] if self.__class__.map_codes else self.__class__.python_type(self.text)'
            
        #     result += '\n'
            
        # else:
            
        #     raise Exception
            
        # result += '\n'
            
        # return result
    
    
    # @property
    # def parse_as_class(self):
    #     ""
    #     #print(' -', self.name, '(element as class)')
        
    #     result = ''
    #     result += f'class {self.class_name}(_Base, etree.ElementBase):\n'
    #     result += f'    ""\n'
                        
    #     result += self.complex_type.parse
        
    #     return result
    
    @property
    def parse_as_method(self):
        ""
        #print('  -', self.name, '(element as method)')
        
        result = ''
        
        result +=  '@property\n'
        result += f'def {self.method_name}(self):\n'
        result += '    ""\n'
        
        if self.is_multiple:
            result += f"    return self.findall('{{{schema_element.target_namespace}}}{self.name}')\n"
        else:
            result += f"    return self.find('{{{schema_element.target_namespace}}}{self.name}')\n"
        
        result += '\n'
        
        return result
    
    
    @property
    def parse_as_method_old(self):
        ""
        #print('  -', self.name, '(element as method)')
        
        result = ''
        
        result +=  '@property\n'
        result += f'def {self.method_name}(self):\n'
        result += f'    """{self.parse_documentation}"""\n'
        
        if self.is_xs_type or self.is_simple_type or self.complex_type.has_simple_content:
            
            if self.is_simple_type:
                map_dict = self.simple_type.map_dict
            else:
                if self.xs_type == 'boolean':
                    map_dict = {'true': True, '1': True, 'false': False, '0': False}
                else:
                    map_dict = {}
            
            if map_dict:
                result += f'    map_ = {str(map_dict)}\n'
            
            if self.is_multiple:
                result += f"    x = self.findall('{{{schema_element.target_namespace}}}{self.name}')\n"
                if map_dict:
                    result += f'    return [{self.python_type_convertor}(map_[e.text]) for e in x]\n'
                else:
                    result += f'    return [{self.python_type_convertor}(e.text) for e in x]\n'
            
            else:
                
                result += f"    e = self.find('{{{schema_element.target_namespace}}}{self.name}')\n"
                result +=  '    if not e is None:\n'
                if map_dict:
                    result += f'        return {self.python_type_convertor}(map_[e.text])\n'
                else:
                    result += f'        return {self.python_type_convertor}(e.text)\n'
                
                if self.is_optional:    
                    result +=  '    else:\n'
                    result +=  '        return None\n'
                    
                else:
                    result +=  '    else:\n'
                    result += f"        raise Exception('{self.method_name}')\n"
                    
            
        elif self.is_complex_type:
            
            if self.is_multiple:
                result += f"    return self.findall('{{{schema_element.target_namespace}}}{self.name}')\n"
            else:
                result += f"    return self.find('{{{schema_element.target_namespace}}}{self.name}')\n"
            
        else:
            
            raise Exception(self.type_name, self.name)
        
        result +=  '\n'
        
        return result
    
    @property
    def parse_documentation(self):
        ""
        if self.has_annotation:
            return self.annotation.parse
        else:
            return ''
    
    @property
    def parse_type_documentation(self):
        ""
        #print('self.is_complex_type', self.is_complex_type)
        if self.is_complex_type:
            #print('self.complex_type.parse_annotation', self.complex_type.parse_annotation)
            return self.complex_type.parse_annotation
        else:
            return ''
        
    @property
    def python_type_convertor(self):
        ""
        if self.is_xs_type:
            xs_type = self.xs_type
        elif self.is_simple_type:
            if self.simple_type.restriction.is_xs_type:
                xs_type = self.simple_type.xs_type
            elif self.simple_type.restriction.is_simple_type:
                xs_type = self.simple_type.restriction.simple_type.xs_type
            else:
                raise Exception
        else:
            xs_type = self.complex_type.simple_content.xs_type
        if not xs_type is None:
            if xs_type == 'string':
                return 'str'
            elif xs_type == 'token':
                return 'str'
            elif xs_type == 'date':
                return 'datetime.date.fromisoformat'
            elif xs_type == 'boolean':
                return 'bool'
            elif xs_type == 'integer':
                return 'int'
            elif xs_type == 'positiveInteger':
                return 'int'
            elif xs_type == 'nonPositiveInteger':
                return 'int'
            elif xs_type == 'nonNegativeInteger':
                return 'int'
            elif xs_type == 'decimal':
                return 'float'
            elif xs_type == 'base64Binary':
                return 'base64.b64encode'
            else:
                raise Exception(xs_type)
            
        else:
            raise Exception
    
    @property
    def simple_type(self):
        ""
        ""
        if self.has_simple_type_child:
            return self.find('{http://www.w3.org/2001/XMLSchema}simpleType')
        else:
            for schema_file_name, root in schema_roots.items():
                x = root.find((f'{{http://www.w3.org/2001/XMLSchema}}simpleType[@name="{self.type_name}"]'))
                if not x is None:
                    return x
        return None 
    
    @property
    def type_name(self):
        ""
        return self.attrib.get('type')
        
    @property
    def version(self):
        ""
        return self.getparent().version
    
    @property
    def xs_type(self):
        ""
        if not self.type_name is None:
            if self.type_name.startswith('xs:'):
                return self.type_name.split(':')[1]
            else:
                return None
        else:
            return None
    


class Enumeration(etree.ElementBase):
    ""    
    @property
    def annotation(self):
        ""
        return self.find('{http://www.w3.org/2001/XMLSchema}annotation')
    
    @property
    def has_annotation(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}annotation')
        if len(x) > 0:
            return True
        else:
            return False
    
    @property
    def item_dict(self):
        ""
        return {self.value:self.parse_documentation}
    
    @property
    def parse_documentation(self):
        ""
        if self.has_annotation:
            return self.annotation.parse
        else:
            return ''
        
    @property
    def value(self):
        ""
        return self.attrib.get('value')



class Extension(etree.ElementBase):
    ""
    @property
    def base(self):
        ""
        return self.attrib.get('base')
    
    @property
    def xs_type(self):
        ""
        if self.base.startswith('xs:'):
            return self.base.split(':')[1]
        else:
            return None
    
    

class Include(etree.ElementBase):
    ""


class Restriction(etree.ElementBase):
    ""
    
    @property
    def base(self):
        ""
        return self.attrib.get('base')
    
    @property
    def enumerations(self):
        ""
        return self.findall('{http://www.w3.org/2001/XMLSchema}enumeration')
    
    @property
    def is_simple_type(self):
        ""
        if not self.simple_type is None:
            return True
        else:
            return False
    
    @property
    def is_xs_type(self):
        ""
        if self.base.startswith('xs:'):
            return True
        else:
            return False
        
    
    @property
    def map_codes(self):
        ""
        d = {}
        for e in self.enumerations:
            d.update(e.item_dict)
        if len(d) == 0:
            return None
        else:
            return d
    
    @property
    def map_values(self):
        ""
        if self.map_codes is None:
            return None
        else:
            return {v:k for k,v in self.map_codes.items()}
        
    @property
    def simple_type(self):
        ""
        for schema_file_name, root in schema_roots.items():
            x = root.find((f'{{http://www.w3.org/2001/XMLSchema}}simpleType[@name="{self.base}"]'))
            if not x is None:
                return x
        else:
            return None
    
    @property
    def xs_type(self):
        ""
        if self.is_xs_type:
            return self.base.split(':')[1]
        else:
            return None
    
    

class Schema(etree.ElementBase):
    ""
    
    @property
    def elements(self):
        "The child elements"
        return self.findall('{http://www.w3.org/2001/XMLSchema}element')
    
    @property
    def parse(self):
        ""
        result = ''
        for e in self.elements:
            
            result += e.parse
            result += '\n'
            
            #break
        
        return result
    
    @property
    def target_namespace(self):
        ""
        return self.attrib.get('targetNamespace')
    
    @property
    def version(self):
        ""
        return self.attrib.get('version')
    
    

    
    

       
    

        
    
class SimpleType(etree.ElementBase):
    ""
    
    @property
    def annotation(self):
        ""
        return self.find('{http://www.w3.org/2001/XMLSchema}annotation')
    
    @property
    def documentation(self):
        ""
        return self.annotation.documentation
        
    @property
    def has_annotation(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}annotation')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def has_documentation(self):
        ""
        if self.has_annotation:
            return self.annotation.has_documentation
        else:
            return False
    
    @property
    def has_restriction(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}restriction')
        if len(x) > 0:
            return True
        else:
            return False
    
    @property
    def map_codes(self):
        ""
        if self.xs_type == 'boolean':
            return {'true': True, '1': True, 'false': False, '0': False}
        elif self.has_restriction:
            return self.restriction.map_codes
        else:
            return None
        
    @property
    def map_values(self):
        ""
        if self.map_codes is None:
            return None
        else:
            return {v:k for k,v in self.map_codes.items()}
        
        
    @property
    def parse(self):
        ""
        result = ''
        
        if self.has_documentation:
            result += f'documentation2 = """{self.documentation.parse}"""\n'
            
        result += f'xs_type = "{self.xs_type}"\n'
        result += f'python_type = {self.python_type_convertor}\n'
        
        map_dict = self.map_dict
        result += f'map_codes = {str(map_dict)}\n'
        map_dict2 = {v:k for k,v in map_dict.items()}
        result += f'map_values = {str(map_dict2)}\n'
        
        result += '\n'
        result += '@property\n'
        result += 'def value(self): return self.__class__.map_codes[self.text] if self.__class__.map_codes else self.__class__.python_type(self.text)'
        
        result += '\n'
        
        return result
        
        
    @property
    def python_type_convertor(self):
        ""
        xs_type = self.xs_type
        if not xs_type is None:
            if xs_type == 'string':
                return 'str'
            elif xs_type == 'token':
                return 'str'
            elif xs_type == 'date':
                return 'datetime.date.fromisoformat'
            elif xs_type == 'boolean':
                return 'bool'
            elif xs_type == 'integer':
                return 'int'
            elif xs_type == 'positiveInteger':
                return 'int'
            elif xs_type == 'nonNegativeInteger':
                return 'int'
            elif xs_type == 'decimal':
                return 'float'
            elif xs_type == 'base64Binary':
                return 'base64.b64encode'
            else:
                raise Exception(xs_type)
            
        else:
            raise Exception
        
    @property
    def restriction(self):
        ""
        return self.find('{http://www.w3.org/2001/XMLSchema}restriction')
            
    
    @property
    def xs_type(self):
        ""
        if self.has_restriction:
            return self.restriction.xs_type
        else:
            return None
        
        
    

    

    
    
    
class Sequence(etree.ElementBase):
    ""
    
    @property
    def parse(self):
        ""
        l = []
        
        for e in self:
            
            if e.tag == '{http://www.w3.org/2001/XMLSchema}element':
                
                l.append(e.parse)
                
            elif e.tag == '{http://www.w3.org/2001/XMLSchema}choice':
                
                l.extend(e.parse)
            
            else:
                
                raise Exception(e.tag)
        
        return l
    
    
    

    
    
 
    


        
    
        
class SimpleContent(etree.ElementBase):
    ""
    
    @property
    def annotation(self):
        ""
        return self.find('{http://www.w3.org/2001/XMLSchema}annotation')
    
    @property
    def documentation(self):
        ""
        return self.annotation.documentation
        
    @property
    def has_annotation(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}annotation')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def has_documentation(self):
        ""
        if self.has_annotation:
            return self.annotation.has_documentation
        else:
            return False
    
    @property
    def extension(self):
        ""
        return self.find('{http://www.w3.org/2001/XMLSchema}extension')
    
    def has_extension(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}extension')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def has_restriction(self):
        ""
        x = self.findall('{http://www.w3.org/2001/XMLSchema}restriction')
        if len(x) > 0:
            return True
        else:
            return False
        
    @property
    def map_codes(self):
        ""
        if self.xs_type == 'boolean':
            return {'true': True, '1': True, 'false': False, '0': False}
        elif self.has_restriction:
            return self.restriction.map_codes
        else:
            return None
        
    @property
    def map_values(self):
        ""
        if self.map_codes is None:
            return None
        else:
            return {v:k for k,v in self.map_codes.items()}
        
    @property
    def parse(self):
        ""
        result = ''
        
        if self.has_documentation:
            result += f'documentation2 = """{self.documentation.parse}"""\n'
            
        result += f'xs_type = "{self.xs_type}"\n'
        result += f'python_type = {self.python_type_convertor}\n'
        
        map_dict = self.map_dict
        result += f'map_codes = {str(map_dict)}\n'
        map_dict2 = {v:k for k,v in map_dict.items()}
        result += f'map_values = {str(map_dict2)}\n'
        
        result += '\n'
        result += '@property\n'
        result += 'def value(self): return self.__class__.map_codes[self.text] if self.__class__.map_codes else self.__class__.python_type(self.text)'
        
        result += '\n'
        
        return result
    
    @property
    def python_type_convertor(self):
        ""
        xs_type = self.xs_type
        if not xs_type is None:
            if xs_type == 'string':
                return 'str'
            elif xs_type == 'token':
                return 'str'
            elif xs_type == 'date':
                return 'datetime.date.fromisoformat'
            elif xs_type == 'boolean':
                return 'bool'
            elif xs_type == 'integer':
                return 'int'
            elif xs_type == 'positiveInteger':
                return 'int'
            elif xs_type == 'nonNegativeInteger':
                return 'int'
            elif xs_type == 'decimal':
                return 'float'
            elif xs_type == 'base64Binary':
                return 'base64.b64encode'
            else:
                raise Exception(xs_type)
            
        else:
            raise Exception
    
    @property
    def xs_type(self):
        ""
        if self.has_extension:
            return self.extension.xs_type
        else:
            return None
        

        

        
        

#%% --- set up parser ---    

class MyLookup(etree.CustomElementClassLookup):
    ""
    def lookup(self, node_type, document, namespace, name):
        if node_type == 'element':
            class_name = name.replace(':','_')
            class_name = class_name[0].upper() + class_name[1:]
            return globals()[class_name]
            
        else:
            #raise Exception(node_type)
            return None 
        
def get_parser():
    ""        
    parser = etree.XMLParser()
    parser.set_element_class_lookup(MyLookup())
    return parser

#%% --- set up lookup dict to access roots of all .xsd files ---

def schema_name(schema_dir_name):
    ""
    return schema_dir_name.replace('.','_').replace('-','_')

def schema_version(schema_dir_name):
    ""
    return schema_dir_name.replace('SAP-Schema-','')



def get_schema_roots(schema_dir_name, parser):
    ""
    # data_folder
    if 'SAP' in os.listdir(os.path.join('_schemas', schema_dir_name)):
        data_folder = os.path.join(
            '_schemas',
            schema_dir_name,
            'SAP'
            )
    elif 'RdSAP' in os.listdir(os.path.join('_schemas', schema_dir_name)):
        data_folder = os.path.join(
            '_schemas',
            schema_dir_name,
            'RdSAP'
            )
    else:
        data_folder = os.path.join(
            '_schemas',
            schema_dir_name,
            )
        
    # templates_folder
    templates_folder = os.path.join(
        data_folder,
        'Templates')
    
    # UDT folder
    udt_folder = os.path.join(
        data_folder,
        'UDT')
    
    # roots_dict
    d = {}
    for fn in os.listdir(templates_folder):
        fp = os.path.join(templates_folder, fn)
        d[fn] = etree.parse(fp, parser = parser).getroot()
    for fn in os.listdir(udt_folder):
        fp = os.path.join(udt_folder, fn)
        d[fn] = etree.parse(fp, parser = parser).getroot()
        
    return d



#%% --- main function ---

import_statements = """import datetime
import base64
from lxml import etree
from copy import deepcopy
"""

class_Base_text = """
class _Base():
    ""
    def __repr__(self):
        ""
        return f'<{self.__class__.__name__} {self.tag}>'


    def copy(self):
        ""
        # get root and path to element
        path = []
        element = self
        while True:
            parent = element.getparent()
            if parent is None:
                break
            position = list(parent).index(element)
            path.insert(0,position)
            element = parent
            #break
        path
        root = element

        copy_root = deepcopy(root)  # only works for the root element...

        # get copied element

        copy_element = copy_root
        for i in path:
            copy_element = copy_element[i]

        copy_self = copy_element

        return copy_self


    def display(self, show_values = True):
        ""

        copy_self = self.copy()

        if show_values:

            for element in copy_self.iter():

                if not element.map_codes is None:

                    value = element.map_codes.get(element.text)

                    if not value is None:

                        element.text = f"{element.text} ['{value}']"

        return etree.tostring(copy_self, pretty_print=True).decode()
    
    
    @property
    def sap_xml_properties(self):
        ""
        return ['code', 'value', 'sap_xml_codes'] + self.subclass_method_names


    @property
    def sap_xml_methods(self):
        ""
        return (
            ['copy', 'display'] 
            + [f'add_{x}' for x in self.sap_xml_properties if not x in ['code', 'value', 'sap_xml_codes']]
            )


    @property
    def sap_xml_codes(self):
        ""
        return self.map_codes


"""

def main():
    """
    
    - Loops through the XML schemas in folder 'schemas'
    - For each group of .xsd files, creates an Python autoclass .py file.
    
    """
    
    schema_group_dir_names = os.listdir('_schemas')
    print(schema_group_dir_names)

    for schema_group_dir_name in schema_group_dir_names:

        if not (schema_group_dir_name.startswith('SAP') 
            or schema_group_dir_name.startswith('RdSAP')
            ):
            continue
        
        print(schema_group_dir_name, '(schema_group_dir_name)')
        
        global version
        version = schema_version(schema_group_dir_name)
        
        parser = get_parser()
        
        global schema_roots
        schema_roots = get_schema_roots(schema_group_dir_name, parser)
        
        
        if schema_group_dir_name == 'RdSAP-Schema-21.0.0':
            schema_file_name = 'RdSAP-Report.xsd'
        elif schema_group_dir_name == 'SAP-Schema-18.0.0':
            schema_file_name = 'SAP-Report.xsd'
        else:
            schema_file_name = 'SAP-Compliance-Report.xsd'
        
        global schema_element   
        schema_element = schema_roots[schema_file_name]
        
        if schema_group_dir_name == 'RdSAP-Schema-21.0.0':
            root_element = schema_element.find((f'{{http://www.w3.org/2001/XMLSchema}}element[@name="RdSAP-Report"]'))
        elif schema_group_dir_name == 'SAP-Schema-18.0.0':
            root_element = schema_element.find((f'{{http://www.w3.org/2001/XMLSchema}}element[@name="SAP-Report"]'))
        else:
            root_element = schema_element.find((f'{{http://www.w3.org/2001/XMLSchema}}element[@name="SAP-Compliance-Report"]'))
        
        d = root_element.parse
        d['parent_class_name'] = None
        
        print(d)
        
        
        # create result
        result = ""
        result += import_statements
        result += class_Base_text
        result += class_dict_to_code(d)
        
        
        # save result
        fp = os.path.join(
            #'auto_classes',
            f'classes_{schema_name(schema_group_dir_name)}.py'
            )
        with open(fp, 'w') as f:
            f.write(result)
            
        #break
    

def class_dict_to_code(d):
    ""
    
    print(d['name'])
    
    result = ''
    
    result += f'class {d["class_name"]}(_Base, etree.ElementBase):\n'
    result += '    ""'
    result += '\n'
    
    result += f'    element_name = "{d["name"]}"\n'
    result += f'    namespace = "{schema_element.target_namespace}"\n'
    result += f'    element_type = "{d["type"]}"\n'
    result += f'    class_name = "{d["class_name"]}"\n'
    
    if d['documentation'] is None:
        result += f'    documentation = None\n'
    else:
        result += f'    documentation = """{d["documentation"]}"""\n'
    if d['subclass_dict']['documentation'] is None:
        result += f'    type_documentation = None\n'
    else:
        result += f'    type_documentation = """{d["subclass_dict"]["documentation"]}"""\n'
    result += f'    has_text_node = {d["has_text_node"]}\n'
    result += f'    min_occurs = {d["min_occurs"]}\n'
    if d['max_occurs'] == 'unbounded':
        result += f'    max_occurs = "{d["max_occurs"]}"\n'
    else:
        result += f'    max_occurs = {d["max_occurs"]}\n'
    result += f'    python_type_convertor = {d["python_type_convertor"]}\n'
    result += f'    map_codes = {d["map_codes"]}\n'
    result += f'    map_values = {d["map_values"]}\n'
    
    if d['parent_class_name'] is None:
        result += f'    parent_class_name = {d["parent_class_name"]}\n'
        result += '    parent_method_name = None\n'
    else:
        result += f'    parent_class_name = "{d["parent_class_name"]}"\n'
        parent_method_name = d['parent_class_name'].lower()
        if parent_method_name in ['property']:
            parent_method_name += '_'
        result += f'    parent_method_name ="{parent_method_name}"\n'
            
    subclass_class_names = [x['class_name'] for x in d['subclass_dict']['subclasses']]
    if len(subclass_class_names) > 0:
        subclass_class_names_string = '"' + '", "'.join(subclass_class_names) + '"' 
    else:
        subclass_class_names_string = ''
    result += f'    subclass_class_names = [{subclass_class_names_string}]\n'
    
    subclass_method_names = [x.lower() for x in subclass_class_names]
    if len(subclass_method_names) > 0:
        subclass_method_names_string = '"' + '", "'.join(subclass_method_names) +'"'
    else:
        subclass_method_names_string = ''
    result += f'    subclass_method_names = [{subclass_method_names_string}]\n'
        
    result += '\n'
    
    if not d['parent_class_name'] is None:
        result += f'    @property\n'
        result += f'    def {parent_method_name}(self): return self.getparent()\n'
        result += '\n'
        
    for subclass in d['subclass_dict']['subclasses']:
        subclass_name = subclass['name']
        subclass_class_name = subclass['class_name']
        subclass_method_name = subclass_class_name.lower()
        if subclass_method_name in ['property']:
            subclass_method_name += '_'
        min_occurs = subclass['min_occurs']
        max_occurs = subclass['max_occurs']
        
        result += f'    @property\n'
        if max_occurs == 1:
            result += f'    def {subclass_method_name}(self): return self.find(f"{{{{{{self.__class__.namespace}}}}}}{subclass_name}")\n'
        else:
            result += f'    def {subclass_method_name}(self): return self.findall(f"{{{{{{self.__class__.namespace}}}}}}{subclass_name}")\n'
        
        result += '\n'
        
        #result += f'    @property\n'
        result += f'    def add_{subclass_method_name}(self):\n'
        result += f'        return etree.SubElement(self,f"{{{{{{self.__class__.namespace}}}}}}{subclass_name}")\n'
        result += '\n'
        
        
        
        
    if d['has_text_node'] == True:
        result += f'    @property\n'
        if d['map_codes'] is None:
            if d['python_type_convertor'] == 'str':
                result += '    def value(self): return self.text\n'
            else:
                result += '    def value(self): return self.__class__.python_type_convertor(self.text)\n'
        else:
            result += '    def value(self): return self.__class__.map_codes[self.text]\n'
        result += '\n'
        
        result += f'    @value.setter\n'
        if d['map_codes'] is None:
            result += '    def value(self, value): self.text = str(value)\n'
        else:
            result += '    def value(self, value):\n'
            result += '        if value in self.__class__.map_values:\n'
            result += '            self.text = self.__class__.map_values[value] if self.__class__.python_type_convertor == bool else self.__class__.map_values[str(value)]\n' 
            result += '        else:\n'
            result += f"""            raise ValueError(f'value "{{value}}" is not in "{{str(list(self.__class__.map_values))}}")')\n"""
        result += '\n'
        
        result += f'    @property\n'
        result += '    def code(self): return self.text\n'
        result += '\n'
    
        result += f'    @code.setter\n'
        if d['map_codes'] is None:
            result += '    def code(self, code): self.text = str(code)\n'
        else:
            result += '    def code(self, code):\n'
            result += '        if code in self.__class__.map_codes:\n'
            result += '            self.text = str(code)\n'
            result += '        else:\n'
            result += f"""            raise ValueError(f'code "{{code}}" is not in "{{str(list(self.__class__.map_codes))}}")')\n"""
        result += '\n'
        
        
    for subclass in d['subclass_dict']['subclasses']:
        
        subclass['parent_class_name'] = d["class_name"]
        
        x = class_dict_to_code(subclass)
        result += '    ' + '\n    '.join(x.split('\n')[:-1]) + '\n'
        
    
    
    return result



if __name__ == '__main__':
    
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    