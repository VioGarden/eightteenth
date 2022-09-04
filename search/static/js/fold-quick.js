//function that opens a flap/dropdown for extra information about a song
function show(element) {
    if(element.nextElementSibling.classList.contains('wrapper-hidden')){
        element.nextElementSibling.classList.remove('wrapper-hidden')
    } else {
        element.nextElementSibling.classList.add('wrapper-hidden')
    }
}