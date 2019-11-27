function showFile(){
  filename = document.getElementById('file').files.item(0).name;
  document.getElementById('filespan').innerHTML = filename;
}
