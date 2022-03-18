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
  hide_section('location');
  hide_section('save_object');
  updatePage();
});

function detectObject() {
  try {
    if (intervalID)
      clearInterval(intervalID);
  } catch (error) {}

  let the_object=document.getElementById('object').value;
  fetch('/set_object?object='+the_object);
  intervalID = setInterval(updatePage,500);
}

function updatePage() {
  updateImage();
  let the_object=document.getElementById('object').value;
  let the_message=document.getElementById('early_result');
  if (""==the_object) {
    try {
      if (intervalID)
        clearInterval(intervalID);
    } catch (error) {}
    hide_section('location');
    hide_section('save_object')
    reveal_section('early_result');
    the_message.innerHTML="No object selected."
    return
  }

  fetch('/object_found')
    .then(response=>response.json())
    .then(function(response){
      console.log(response);
      if ("True"==response) {
        clearInterval(intervalID);
        hide_section('early_result');
        reveal_section('save_object');
        reveal_section('location');
        getCoords();
      }
      else {
        hide_section('location');
        hide_section('save_object');
        reveal_section('early_result');
        the_message.innerHTML="Looking for object...";
      }
    })
}

function updateImage() {
  document.getElementById('webcam_image').src='/get_cam?=' + new Date().getTime();
}

function getCoords() {
  fetch('/get_coords')
    .then(response=>response.json())
    .then(function(response){
      inject_response(response,'location_data');
  })
  fetch('/get_raw_coords')
    .then(response=>response.json())
    .then(function(response){
      console.log(response);
      document.getElementById('raw_coords').innerHTML=response;
    })
}

function save_object() {
  hide_section('save_object');
  let the_object=document.getElementById('object').value;
  fetch('/save_object?object='+the_object);
}

function inject_response(response,tableID) {
  console.log('injecting coords')
  let theTable=document.getElementById(tableID);

  let rowCount = theTable.rows.length;
  for (let i = 0; i < rowCount; i++) {
      theTable.deleteRow(0);
  }
  console.log('injecting coords')
  let theRow = theTable.insertRow();
  for (i=0;i<3;i++) {
    theRow.insertCell().innerHTML=response[i];
  }
}

function reveal_section(item) {
  var r = document.getElementById(item);
  if (r.style.display == "none") {
    r.style.display = "";
    // https://www.w3schools.com/jsref/prop_style_display.asp
  }
}

function hide_section(item) {
  var s = document.getElementById(item);
    s.style.display = "none";
}
