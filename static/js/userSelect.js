var ip;
function init() {
  if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    window.location.href="/mobileUserSelect";
  }
  // document.getElementById('uploader').action = "http://" + ip + "/uploader";
//   window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;//compatibility for Firefox and chrome
//   var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};
//   pc.createDataChannel('');//create a bogus data channel
//   pc.createOffer(pc.setLocalDescription.bind(pc), noop);// create offer and set local description
//   pc.onicecandidate = function(ice, ip)
//   {
//    if (ice && ice.candidate && ice.candidate.candidate)
//    {
//     ip = /([0-9]{1,3}(\.[0-9]{1,3}){3})/.exec(ice.candidate.candidate)[1];
//     // window.location.href = '/users?ip=' + ip;
//     adminIp = '10.96.4.60';
//     if (ip == adminIp){
//       console.log('test');
//       // window.location.href = "/home";
//     }else{
//       window.location.href = "/";
//     }
//   }
// }
}
window.onload = init();
function redir(x){
  // console.log(x.innerHTML);
  $.removeCookie("ip");
  $.cookie("ip", x.innerHTML);
  var url = "/admin?ip=" + x.innerHTML;
  window.location.href=url;
}
function users() {
    window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;//compatibility for Firefox and chrome
    var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};
    pc.createDataChannel('');//create a bogus data channel
    pc.createOffer(pc.setLocalDescription.bind(pc), noop);// create offer and set local description
    pc.onicecandidate = function(ice, ip)
    {
     if (ice && ice.candidate && ice.candidate.candidate)
     {
      ip = /([0-9]{1,3}(\.[0-9]{1,3}){3})/.exec(ice.candidate.candidate)[1];
      window.location.href = '/users?ip=' + ip;
    }
    // Clear forms here
    // document.getElementById("file").value = "";
    // val = document.getElementById('ipadd').innerHTML + ip;
    // document.getElementById("ipadd").innerHTML = val;
}
}
