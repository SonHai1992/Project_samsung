
//show image cam view
function displayPicture(img_url) {
    let main_img = document.getElementById('image_2');
    main_img.src = img_url;

}
function display_Picture(img_url) {
    let main_img = document.getElementById('image_3');
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