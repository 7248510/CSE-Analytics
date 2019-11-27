const urlParams = new URLSearchParams(window.location.search);
const ip = urlParams.get('ip');
console.log(ip);
// window.onload = window.location.href="/scanResults?ip=" + ip;
