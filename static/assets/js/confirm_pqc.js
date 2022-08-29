
function displayPicture(img_url) {
    let main_img = document.getElementById('image_2');
    main_img.src = img_url;

}

 function showPicture(img) {
    let image_instance = document.getElementById(img);
    let img_url = image_instance.src;
    let show_div = document.getElementById('show_img');
    let main_img = document.getElementById('main_img');
    main_img.src = img_url;
    show_div.style.display = "block";
}

function hidePicture() {
    let show_div = document.getElementById('show_img');
    show_div.style.display = "none";
}


function checkFileName(id) {
   let fileinput = document.getElementById(id);
   let filename = fileinput.files[0].name
   let message_element = document.getElementById("message");
   let white_list =  ["xlsx", "xls", "pdf",'pptx','docx','doc']
   let file_extension = filename.split(".").at(-1)

   if (filename && !white_list.includes(file_extension)){
        message_element.innerHTML = `File invalid. Allow ${white_list}`;
        message_element.classList.add("alert", "alert-danger");
        fileinput.value = null;
   }else{
        message_element.innerHTML = "";
        message_element.classList.remove("alert", "alert-danger");
   }
}
function checkFileName_jpg(id) {
   let fileinput = document.getElementById(id);
   let filename = fileinput.files[0].name
   let message_element = document.getElementById("message");
   let white_list = ["jpg","JPN","jpn"]
   let file_extension = filename.split(".").at(-1)

   if (filename && !white_list.includes(file_extension)){
        message_element.innerHTML = `File invalid. Allow ${white_list}`;
        message_element.classList.add("alert", "alert-danger");
        fileinput.value = null;
   }else{
        message_element.innerHTML = "";
        message_element.classList.remove("alert", "alert-danger");
   }
}


//<!--    function reason_control() {-->
//<!--        let status = document.getElementById("status")-->
//
//<!--        if (status.value == "NG") {-->
//<!--            reason.style.display = "block";-->
//<!--        }else{-->
//<!--            reason.style.display = "none";-->

