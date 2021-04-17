function PrefixInteger(num, length) {
 return (Array(length).join('0') + num).slice(-length);
}

const o = new Date();
const y = o.getFullYear()
const m = o.getMonth() + 1
document.getElementById("postMonth").innerHTML = y.toString() + '-' + PrefixInteger(m, 2)

