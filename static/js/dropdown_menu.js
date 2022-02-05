let username = document.querySelector('#username');
let dropdown = document.querySelector('#dropdown');
username.addEventListener('click', (event) => {
    event.preventDefault();
    dropdown.classList.toggle('dropdown_show');
})