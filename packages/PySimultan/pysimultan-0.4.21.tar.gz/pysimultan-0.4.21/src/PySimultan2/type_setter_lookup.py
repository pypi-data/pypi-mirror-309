import numpy as np
import pandas as pd

from .utils import (SimComponent, SimultanObject, SimDoubleParameter, SimIntegerParameter, SimStringParameter,
                    SimBoolParameter, SimEnumParameter, SimMultiValueField3D, SimMultiValueBigTable, FileInfo,
                    set_property_to_sim_component, set_property_to_parameter, set_property_to_value_field,
                    set_property_to_file_info, set_property_to_list, set_property_to_dict)

from .default_types import ComponentList, ComponentDictionary

from SIMULTAN.Data.Components import (ComponentWalker, SimComponent, SimBoolParameter, SimDoubleParameter,
                                      SimEnumParameter, SimIntegerParameter, SimStringParameter, ComponentMapping,
                                      SimSlot, SimComponentVisibility, SimChildComponentEntry, SimDefaultSlots,
                                      SimParameterOperations, SimComponentReference)


lookup_dict = {None: lambda x: None,
               SimComponent: set_property_to_sim_component,
               SimultanObject: set_property_to_sim_component,
               SimDoubleParameter: set_property_to_parameter,
               SimIntegerParameter: set_property_to_parameter,
               SimStringParameter: set_property_to_parameter,
               SimBoolParameter: set_property_to_parameter,
               SimEnumParameter: set_property_to_parameter,
               SimMultiValueField3D: set_property_to_value_field,
               SimMultiValueBigTable: set_property_to_value_field,
               int: set_property_to_parameter,
               float: set_property_to_parameter,
               str: set_property_to_parameter,
               bool: set_property_to_parameter,
               FileInfo: set_property_to_file_info,
               list: set_property_to_list,
               tuple: set_property_to_list,
               set: set_property_to_list,
               dict: set_property_to_dict,
               ComponentDictionary: set_property_to_dict,
               ComponentList: set_property_to_list,
               np.ndarray: set_property_to_value_field,
               pd.DataFrame: set_property_to_value_field}


class TypeSetterFcnLookupDict(object):

    def __getitem__(self, item: type):
        if item in lookup_dict:
            return lookup_dict[item]
        elif SimultanObject in item.__bases__:
            return set_property_to_sim_component
        else:
            return None

    def get(self,
            item: type,
            default=None):
        val = self.__getitem__(item)
        if val is None:
            return default
        else:
            return val


type_setter_fcn_lookup_dict = TypeSetterFcnLookupDict()
