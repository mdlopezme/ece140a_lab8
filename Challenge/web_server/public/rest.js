document.addEventListener("DOMContentLoaded", function() {
  console.log('Document Loaded')
  object_select=document.getElementById('object')
  fetch('/objects')
    .then(response=>response.json())
    .then(function(response){
      for(index in response){
        var new_option = document.createElement('option');
        new_option.value = response[index];
        new_option.innerHTML = response[index];
        object_select.appendChild(new_option);
      }
    })
  // var intervalID = setInterval(update_webcam, 500);
  // var intervalID = setInterval(updatePage,2000)
  hide_section('location')
  updatePage()
});

function detectObject() {
  let the_object=document.getElementById('object').value
  fetch('/set_object?object='+the_object)
  intervalID = setInterval(updatePage,2000)
}

function updatePage() {
  updateImage();
  let the_object=document.getElementById('object').value;
  let the_message=document.getElementById('early_result');
  reveal_section('early_result');
  if (""==the_object) {
    the_message.innerHTML="No object selected."
    return
  }

  // the_message.innerHTML=""
  fetch('/object_found')
    .then(response=>response.json())
    .then(function(response){
      console.log(response);
      if ("True"==response) {
        clearInterval(intervalID);
        hide_section('early_result');
        getCoords();
      }
      else {
        the_message.innerHTML="Looking for object...";
      }
    })
}

function updateImage() {
  // let the_image = document.getElementById('webcam_image').src;
  // the_image.src='/get_cam?' + new Date().getTime();
  // the_image.src='/get_cam?';
  document.getElementById('webcam_image').src='/get_cam?=' + new Date().getTime();
}

function getCoords() {
  reveal_section('location')
  fetch('/get_coords')
  .then(response=>response.json())
  .then(function(response){
    console.log(response);
  })
}

function reveal_section(item) {
  var r = document.getElementById(item);
  if (r.style.display == "none") {
    r.style.display = "block";
  }
}

function hide_section(item) {
  var s = document.getElementById(item);
    s.style.display = "none";
}