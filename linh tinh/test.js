function update_o_ComposerTextInput_textarea() {
    if (document.getElementsByClassName('o_ComposerTextInput_textarea').length > 0) {
        var textarea = document.getElementsByClassName('o_ComposerTextInput_textarea')[0].value;
        var mirroredTextarea =
            document.getElementsByClassName('o_ComposerTextInput_mirroredTextarea')[0].value;
        document.getElementsByClassName('o_ComposerTextInput_textarea')[0].value += '.';
        document.getElementsByClassName('o_ComposerTextInput_mirroredTextarea')[0].value += '.';
        document.getElementsByClassName('o_ComposerTextInput_textarea')[0].click();
        document.getElementsByClassName('o_ComposerTextInput_textarea')[0].value = textarea;
        document.getElementsByClassName('o_ComposerTextInput_mirroredTextarea')[0].value = mirroredTextarea;
        document.getElementsByClassName('o_ComposerTextInput_textarea')[0].click();
    }
}
function update_data_mail_message_tag() {
    try {
        all_selected_ids = document.getElementById("all_text_mail_message_tag").innerHTML;
        ul = document.getElementById("list_mail_message_tag");
        li = ul.getElementsByTagName("li");
        for (i = 0; i & lt; li.length; i++) {
            a = li[i];
            if (!all_selected_ids.includes(a.value.toString())) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }
    catch (err) {
        console.log(err);
    }
}
function click_mail_message_tag(value, id) {
    try {
        document.getElementById("mail_message_tag_ids").innerHTML +=
            document.getElementById("template_mail_message_tag").innerHTML.replace('text_mail_message_tag',
                value).replace('value_mail_message_tag', id);
        document.getElementById("all_text_mail_message_tag").innerHTML += "," + id;
        update_data_mail_message_tag();
        document.getElementById("key_search_mail_message_tag").value = null;
        update_o_ComposerTextInput_textarea();
    }
    catch (err) {
        console.log(err);
    }
}
function click_remove_mail_message_tag(element, value) {
    try {
        value = element.getElementsByClassName("class_mail_message_tag")[0].id;
        document.getElementById("all_text_mail_message_tag").innerHTML =
            document.getElementById("all_text_mail_message_tag").innerHTML.replace("," + value, "");
        update_data_mail_message_tag();
        element.remove();
        update_o_ComposerTextInput_textarea();
    }
    catch (err) {
        console.log(err);
    }
}
function get_mail_message_tag() {
    try {
        update_data_mail_message_tag();
        if (document.getElementById("get_mail_message_tag_count").innerHTML == "") {
            document.getElementById("list_mail_message_tag").innerHTML +=
                document.getElementById("template_item_mail_message_tag").innerHTML;
            document.getElementById("get_mail_message_tag_count").innerHTML = 1;
        }
    }
    catch (err) {
        console.log(err);
    }
}
function search_mail_message_tag() {
    try {
        var input, filter, ul, li, a, i, txtValue;
        input = document.getElementById("key_search_mail_message_tag");
        all_selected_ids = document.getElementById("all_text_mail_message_tag").innerHTML;
        filter = input.value.toUpperCase();
        ul = document.getElementById("list_mail_message_tag");
        li = ul.getElementsByTagName("li");
        for (i = 0; i & lt; li.length; i++) {
            a = li[i];
            txtValue = a.textContent || a.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1 & amp;
            !all_selected_ids.includes(a.value.toString())) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }
    catch (err) {
        console.log(err);
    }
}

if (document.getElementsByClassName('area_mail_message_tag')) {
    var area = document.getElementsByClassName('area_mail_message_tag');
    var check_area = true;
    if (document.getElementsByClassName('class_model').length == 0) {
        check_area = false;
    }
    else if (document.getElementsByClassName('class_model')[0].innerHTML != 'crm_lead') {
        check_area = false;
    }
    else {
        check_area = true;
    }
    if (!check_area) {
        for (let i = 0; i & lt; area.length; i++) {
            area[i].style.display = "none";
        }
    }
}
window.addEventListener('click', function (e) {
    if (document.getElementsByClassName('o_FormRenderer_chatterContainer').length > 0) {
        if (document.getElementsByClassName('o_FormRenderer_chatterContainer')[0].contains(e.target)) {
        } else {
            if (document.getElementsByClassName('click_remove_mail_message_tag').length > 0) {
                if (document.getElementsByClassName('click_remove_mail_message_tag')[0].toString() ==
                    e.target.toString()) { }
                else if (document.getElementsByClassName('o_Chatter_composer').length > 0) {
                    document.getElementsByClassName('o_Chatter_composer')[0].remove();
                }
            }
            else if (document.getElementsByClassName('o_Chatter_composer').length > 0) {
                document.getElementsByClassName('o_Chatter_composer')[0].remove();
            }
        }
    }
});
if (document.getElementsByClassName('o_Composer_buttonSend').length > 0) {
    document.getElementsByClassName('o_Composer_buttonSend')[0].addEventListener("click",
        remove_o_Composer_buttonSend);
    function remove_o_Composer_buttonSend() {
        document.getElementsByClassName('o_Composer_buttonSend')[0].remove();
    }
}