
// check file and image edit_cam
function showPicture(img_url) {
        let main_img = document.getElementById('main_image');
        let ma_img = document.getElementById('img_1');
        main_img.src = img_url;

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
       for(let i =0; i <= fileinput.files.length;i++){
           let filename = fileinput.files[i].name
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
}
