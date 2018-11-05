const requestvar_prefix = '_rct_selected_';

/**
 *
 * @param formId
 * @param jsonArgs
 *
 * TODO: create hidden in function. Not yet feasable because of other function cause by hidden value.
 */
function entryChoiceSetSelection(formId, jsonArgs){
    for(var key in jsonArgs){
        document.getElementById(requestvar_prefix.concat(key)).value=jsonArgs[key];
    }
    document.forms[formId].submit();
}

/**
 *
 * @param formId
 * @param rowIdentifier
 * @param value
 */
function entryMultiChoiceSetSelection(formId, rowIdentifier, value){
    const separator = ';';

    if(!document.getElementById(requestvar_prefix.concat(rowIdentifier)).value){
        document.getElementById(requestvar_prefix.concat(rowIdentifier)).value=value;
    }else{
        var idArray =  document.getElementById(requestvar_prefix.concat(rowIdentifier)).value.split(separator);
        if(idArray.indexOf(value)>-1){
            idArray.splice(idArray.indexOf(value), 1)
            document.getElementById(requestvar_prefix.concat(rowIdentifier)).value = idArray.join(separator);
        }else{
            document.getElementById(requestvar_prefix.concat(rowIdentifier)).value+=';'+value;
        }
    }
    document.forms[formId].submit();
}
