var search_type = document.getElementById("id_search_type");

search_type.addEventListener("change", change_display);

function change_display() {
    if (search_type.value == 'Clients') {
        document.getElementById('clients').style.display="block";
        document.getElementById('referrals').style.display="none";
    } else {
        document.getElementById('referrals').style.display="block";
        document.getElementById('clients').style.display="none";
    }
}