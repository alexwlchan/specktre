function updateColors() {
    var colorA = document.getElementById("colorA").value;
    if (colorA[0] != "#") {
        colorA = "#" + colorA;
    }
    var colorB = document.getElementById("colorB").value;
    if (colorB[0] != "#") {
        colorB = "#" + colorB;
    }
    document.getElementById("colorAgroup").style.backgroundColor = colorA;
    document.getElementById("colorBgroup").style.backgroundColor = colorB;
}

updateColors();

function updateSizes() {
    var sizeClass = document.getElementById("sizeClassControl").value;
    console.log(sizeClass);
    var hght = document.getElementById("height");
    var wth = document.getElementById("width");
    if (sizeClass == "iphone5") {
        hght.value = 1392;
        wth.value = 744;
    } else if (sizeClass == "iphone6") {
        hght.value = 1608;
        wth.value = 852;
    } else if (sizeClass == "iphone6p") {
        hght.value = 2662;
        wth.value = 2662;
    } else if (sizeClass == "ipad") {
        hght.value = 2524;
        wth.value = 2524;
    }
}

document.getElementById("colorAgroup").onchange = function() {updateColors()};
document.getElementById("colorBgroup").onchange = function() {updateColors()};

document.getElementById("sizeClassControl").onchange = function() {updateSizes()};
document.getElementById("height").onchange = function() {
    document.getElementById("sizeClassControl").value = "custom";
}
document.getElementById("width").onchange = function() {
    document.getElementById("sizeClassControl").value = "custom";
}