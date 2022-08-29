
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
   let showimg = document.getElementById(id);
   var foo = document.getElementById("show_image");
    foo.innerHTML = null;
   for(let i=0; i <= fileinput.files.length; i++){
       let filename = fileinput.files[i].name
       let message_element = document.getElementById("message");
       let white_list = ["jpg","JPG","png","PNG"]
       let file_extension = filename.split(".").at(-1)

       var image = document.createElement("img");
        image.src=URL.createObjectURL(fileinput.files[i])
        image.id=i
        image.width=700

       if (filename && !white_list.includes(file_extension)){
            message_element.innerHTML = `File invalid. Allow ${white_list}`;
            message_element.classList.add("alert", "alert-danger");
            fileinput.value = null;
       }else{foo.appendChild(image);
            message_element.innerHTML = "";
            message_element.classList.remove("alert", "alert-danger");
       }
   }
}


