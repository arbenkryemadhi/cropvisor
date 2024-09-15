// crops
let crops_wrapper=document.querySelector(".crop-finder-form .crops");
let crop_finder_btn=document.querySelector(".crop-finder-form button");
let lat=document.getElementById("loc_lat");
let lon=document.getElementById("loc_lon");

// crop_finder_btn.addEventListener("click", (e)=>{
//     e.preventDefault();
//     getData();
// })
  

// async function getData() {
//     const url = `https://pythonapi?date=${date.value}&latitude=${lat}&longitude=${lon}`;
//     try {
//       const response = await fetch(url);
//       if (!response.ok) {
//         throw new Error(`Response status: ${response.status}`);
//       }
  
//       const json = await response.json();
//       console.log(json);
//       fillCrops(json);

//     } catch (error) {
//       console.error(error.message);
//     }
// }


// function fillCrops(json) {
//   crops_wrapper.innerHTML="";
//   json.data.forEach(item => {
//     let crop=document.createElement("div");
//     crop.innerHTML=item.first_name;
//     crops_wrapper.appendChild(crop);  
//   });
// }


// location
let loc_input = document.getElementById('location');
let location_sug=document.querySelector('.location-suggestions');

loc_input.addEventListener('keyup', getLocSugs);

function getLocSugs () {
  location_sug.classList.add('active');

  if(loc_input.value=='') {
    location_sug.classList.remove('active');
  }

  if(loc_input.value!='') {
    fetch(`https://api.geoapify.com/v1/geocode/autocomplete?text=${loc_input.value}&apiKey=7dee4052723e44bd8911e2227728e5fa`)
    .then(function (response) {
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' + response.status);
        return;
      }
      response.json().then(function (data) {
        console.log(data);
        fillLocations(data);
      });
    })
    .catch(function (err) {
      console.log('Fetch Error :-S', err);
    });
  }
}


function fillLocations(data) {
  location_sug.innerHTML='';
  data.features.forEach(item => {
    let loc=document.createElement("div");
    loc.innerHTML=item.properties.formatted;
    loc.setAttribute('onclick', 'selectLocation(this)');
    loc.setAttribute('data-lat', item.properties.lat);
    loc.setAttribute('data-lon', item.properties.lon);
    location_sug.appendChild(loc);
  });
}

function selectLocation(suggestion) {
  loc_input.value=suggestion.innerHTML;
  lat.value=suggestion.dataset.lat;
  lon.value=suggestion.dataset.lon;
  location_sug.classList.remove('active');
}

