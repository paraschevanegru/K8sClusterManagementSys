// Functie generala pentru a apela metoda POST la un url specificat
async function postData(url = '', data = {}) {

  const response = await fetch(url, {
    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'

    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)
  });
  return response.json();
}


// Apelarea metodei POST la /infrastructure pentru crearea planului de executie
function planInfrastructure() {
  postData('/infrastructure', { etapa: "plan" })
    .then(data => {
      console.log(data);
    });
}

// Apelarea metodei POST la /infrastructure pentru crearea infrastructurii
function applyInfrastructure() {
  postData('/infrastructure', { etapa: "apply" })
    .then(data => {
      console.log(data);
    });
}

// Apelarea metodei POST la /infrastructure pentru distrugerea infrastructurii
function destroyInfrastructure() {
  postData('/infrastructure', { etapa: "destroy" })
    .then(data => {
      console.log(data);
    });
}


// Apelarea metodei GET la /createjob? pentru crearea aplicatiei care calculeaza suma a doua numere
document.getElementById("appCalcButton").addEventListener('click', async function (event) {
  event.preventDefault();

  let a = document.getElementById("FirstArgument").value
  let b = document.getElementById("SecondArgument").value

  let params = {
    "a": a,
    "b": b
  };

  let query = Object.keys(params)
    .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
    .join('&');

  let url = '/createjob?' + query;

  await fetch(url, {
    method: 'GET',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'

    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  });

});

// Apelarea metodei GET la /cleanup pentru stergerea aplicatiei care calculeaza suma a doua numere
document.getElementById("appCleanUpButton").addEventListener('click', async function (event) {
  event.preventDefault();

  let url = '/cleanup';

  await fetch(url, {
    method: 'GET',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'

    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  });

});

// Apelarea metodei GET la /mongodb pentru lansarea aplicatiei MongoDB
document.getElementById("DeployMongoDB").addEventListener('click', async function (event) {
  event.preventDefault();

  let url = '/mongodb';

  await fetch(url, {
    method: 'GET',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'

    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  });

});




