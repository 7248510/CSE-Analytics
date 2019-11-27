function init() {
  if( /Window|Mac/i.test(navigator.userAgent) ) {
    window.location.href="/";
  }
}
window.onload = init;
function redir(x){
  // console.log(x.innerHTML);
  $.removeCookie("ip");
  $.cookie("ip", x.innerHTML);
  var url = "/mobileAdmin?ip=" + x.innerHTML;
  window.location.href=url;
}
