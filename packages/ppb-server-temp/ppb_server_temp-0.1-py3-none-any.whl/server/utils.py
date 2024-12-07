import random
import string
import datetime


def generateRandomString():
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(32))
    # return random.randint(1000000000, 9999999999)

def getDictionaryOrObjectValue(obj, *args):
    # Initialize the current value with the first object
    current_value = obj

    # Iterate over each key/attribute name in args
    for key in args:
        try:
            # Attempt to access the current value as a dictionary
            current_value = current_value[key]
        except TypeError:
            # If current_value is not a dictionary, try to access it as an object attribute
            try:
                current_value = getattr(current_value, key)
            except AttributeError as e:
                # If the attribute does not exist, raise a more informative error
                raise AttributeError(
                    f"Key or attribute '{key}' does not exist in the object."
                ) from e
        except KeyError as e:
            # If the key does not exist in the dictionary, raise a more informative error
            raise KeyError(
                f"Key '{key}' does not exist in the dictionary. DATA : {current_value}"
            ) from e

    # Return the final value after traversing all keys/attributes
    return current_value

def transformDate(date_str):
    """
    Convert a date string in the format 'Tue, 27 Feb 2024 14:51:29 GMT' to a datetime object.
    
    Parameters:
    - date_str (str): The date string to convert.
    
    Returns:
    - datetime.datetime: The corresponding datetime object.
    """
    try:
        return datetime.datetime.strptime(date_str,
                                          '%a, %d %b %Y %H:%M:%S GMT')
    except:
        pass

    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except:
        pass

    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        pass

    try:
        return datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
    except:
        pass


def updateData(dataToUpdate, updateQuery, unupdatableKeys):

    def set_nested(data, key, value):
        keys = key.split('.')
        for k in keys[:-1]:
            data = data.setdefault(k, {})
        data[keys[-1]] = value

    for key, value in updateQuery.items():
        if key in unupdatableKeys:
            raise ValueError(f'{key} is not updatable')
        firstKey = key.split('.')[0]
        if firstKey not in dataToUpdate.keys():
            raise ValueError(f'{key} is not a valid parameter')

        # if it has a dot, it means it is a nested object
        if '.' in key:
            set_nested(dataToUpdate, key, value)
        else:
            dataToUpdate[key] = value
    return dataToUpdate


def validateParameterData(data, keyValuePairs, classInvoker):
    lengthOfData = len(data)
    count = 0
    parameterError = []

    allDataKeys = []
    for key, value in data.items():
        allDataKeys.append(key)

    for key, value in keyValuePairs.items():
        if key == '_id':
            continue
        if key not in allDataKeys:
            raise ValueError(f'{classInvoker} ,{key} is not in data')

    for key, value in data.items():
        foundKey = False
        for key2, value2 in keyValuePairs.items():
            if key == key2:

                foundKey = True
                if not isinstance(value, value2):
                    raise ValueError(f'{key} must be a {value2}')
                if isinstance(value, str):
                    if value != None:
                        if value.strip() == '':
                            raise ValueError(
                                f'{key} must not be an empty string')

                break

        if foundKey == True:
            count += 1
        else:
            parameterError.append(
                f'Error in class {classInvoker}, {key} is not a valid parameter'
            )

    if parameterError != []:
        raise Exception(str(parameterError))

    if count != lengthOfData:
        raise Exception(
            f'{classInvoker}, A parameter was not validated. Please validate all parameters... Its also possible that you misspelled a parameter'
        )
    