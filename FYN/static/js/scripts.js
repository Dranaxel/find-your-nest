
// ###################################################################################
// ###################################################################################
// #### FAVORITE ON LIST PAGE 
// ###################################################################################
// ###################################################################################

if (document.getElementsByClassName("jsBtnFav")) {  //is on result page ?

    let jsBtnFav = document.getElementsByClassName("jsBtnFav")
    let loader = `
    <div class="spinner-border" role="status">
    <span class="sr-only">Loading...</span>
    </div>
`
    let btnText = "Ajouter aux favoris"
    let isLoading = false;

    for (let i = 0; i <= jsBtnFav.length - 1; ++i) {
        jsBtnFav[i].addEventListener('click', (event) => {
            event.preventDefault();
            jsBtnFav[i].innerHTML = loader;
            jsBtnFav[i].setAttribute('disabled', "");
            isLoading = true;
            let favId = jsBtnFav[i].dataset.value;
            let alertDiv = jsBtnFav[i].parentNode.parentNode.parentNode.parentNode.getElementsByClassName('alertFav')[0];

            fetch(`http://localhost:8080/getFavorite/${favId}`, {
                method: "POST"
            }).then(data => {
                data.json().then(json => {

                    if (isLoading) {
                        jsBtnFav[i].innerHTML = btnText;
                        jsBtnFav[i].removeAttribute('disabled');
                    }

                    if (json.is) {
                        alertDiv.innerHTML = buildAlert(json.msg, "success")
                        setTimeout(() => {
                            alertDiv.innerHTML = ""
                        }, 2000)
                    } else {
                        alertDiv.innerHTML = buildAlert(json.msg, "warning")
                        setTimeout(() => {
                            alertDiv.innerHTML = ""
                        }, 2000)
                    }
                })
            })
        })
    }

}

// ###################################################################################
// ###################################################################################
// #### FAVORITE ON SINGLE PAGE 
// ###################################################################################
// ###################################################################################

if (document.getElementById("jsBtnFav")) {  //is on result page ?

    let jsBtnFav = document.getElementById("jsBtnFav")
    let loader = `
        <div class="spinner-border" role="status">
            <span class="sr-only">Loading...</span>
        </div>
    `
    let btnText = "Ajouter aux favoris"
    let isLoading = false;


    jsBtnFav.addEventListener('click', (event) => {
        event.preventDefault();
        jsBtnFav.innerHTML = loader;
        jsBtnFav.setAttribute('disabled', "");
        isLoading = true;
        let favId = jsBtnFav.getAttribute("data-value");
        let alertDiv = jsBtnFav.parentNode.parentNode.parentNode.parentNode.parentNode.getElementsByClassName('alertFav')[0];
console.log(favId)
        fetch(`http://localhost:8080/getFavorite/${favId}`, {
            method: "POST"
        }).then(data => {
            data.json().then(json => {

                if (isLoading) {
                    jsBtnFav.innerHTML = btnText;
                    jsBtnFav.removeAttribute('disabled');
                }

                if (json.is) {
                    alertDiv.innerHTML = buildAlert(json.msg, "success")
                    setTimeout(() => {
                        alertDiv.innerHTML = ""
                    }, 2000)
                } else {
                    alertDiv.innerHTML = buildAlert(json.msg, "warning")
                    setTimeout(() => {
                        alertDiv.innerHTML = ""
                    }, 2000)
                }
            })
        })
    })
}

// ###################################################################################
// ###################################################################################
// #### LOADER 
// ###################################################################################
// ###################################################################################

if (document.getElementById("map")) { // if is on main page

    let btn1 = document.getElementById("btn-1");

    btn1.addEventListener('click', () => {
        let carte = document.getElementsByClassName("lightbox")
        carte[0].style.display = "flex"
    })
}


// ###################################################################################
// ###################################################################################
// #### MORE METHOD 
// ###################################################################################
// ###################################################################################

function buildAlert(msg, type) {
    return `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
        `
}