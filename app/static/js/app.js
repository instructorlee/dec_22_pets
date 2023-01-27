/* Events */



var loggedUser = null;
var pets = []

startApp = () => {

    setLoggedUser(null);
    setEvents();
    setPage('login');
}

setPage = ( pageID ) => {

    // hide all pages
    document.querySelectorAll('.page')
        .forEach( page => { page.style.display='none' })

    // show selected page
    document.getElementById( pageID ).style.display='flex';

    switch (pageID) {
        case 'dashboard':
            setDashboard();
            break;
    }
}

setLoggedUser = ( userData ) => { 

    loggedUser = userData;

    if ( userData ) { 

        document.querySelectorAll('.user_name')
            .forEach( element => { element.innerHTML = userData['first_name'] })

        document.getElementById('menu_bar').style.display='flex';

    } else {

        document.getElementById('menu_bar').style.display='none';
    }
}

setEvents = () => {

    let loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();

        let formData = new FormData(loginForm);
        
        fetch('/api/user/login', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  'email_address': formData.get('email_address'),
                  'password': formData.get('password')
              })
        })
        .then( response => {
            switch( response.status ) {

                case 200: // OK
                    return response.json();

                default:
                    window.alert('Invalid Login')
            }
        })
        .then( data => {
            completeLogin(data)
        } )
        .catch( data => {
            console.log(`error: ${data}`)
        })
    })

    let registerForm = document.getElementById('registerForm');
    registerForm.addEventListener('submit', (e) => {
        e.preventDefault();
        let formData = new FormData(registerForm);
        
        fetch('/api/user/register', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  'email_address': formData.get('email_address'),
                  'password': formData.get('password'),
                  'password_confirm': formData.get('password_confirm'),
                  'first_name': formData.get('first_name'),
                  'last_name': formData.get('last_name')
              })
        })
        .then( response => { console.log(JSON.stringify(response.body))
            switch( response.status ) {

                case 422: // validation issue
                    return response.json();

                case 200: // OK
                    setPage('login');
                    break;

                default:
                    window.alert(JSON.parse(response.json()))
            }
        })
        .then( data => {
            window.alert(data['errors'].join('\n'))
        })
        .catch( data => {
            console.log(`error: ${data}`)
        })
    })

    let addPetForm = document.getElementById('addPetForm');
    addPetForm.addEventListener('submit', (e) => {
        e.preventDefault();
        let formData = new FormData(addPetForm);
        
        fetch('/api/pet/add', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  'name': formData.get('name'),
                  'age': formData.get('age'),
                  'type': formData.get('type'),
                  'hobby': formData.get('hobby'),
                  'favorite_snack': formData.get('favorite_snack')
              })
        })
        .then( response => { 
            return response.json();
        })
        .then ( data => {
            pets.push(data)
            setPage('dashboard');
        })
        .catch( data => {
            console.log(`error: ${data}`)
        })
    })
}

completeLogin = ( userData ) => {

    setLoggedUser(userData);

    // load pets
    fetch('/api/pet')
    .then( response => response.json() )
    .then( data => { 
        pets = data;
        setPage('dashboard');
    } )
    .catch( data => {
        console.log(`error: ${data}`)
    }) 
}

setDashboard = () => { 
console.log(pets)
    // take list of animals and create HTML
    let html = "";
    pets.forEach( pet => {
        html += '<tr>';
        html += `<td>${pet.name}</td>`;
        html += `<td>${pet.type}</td>`;
        html += `<td>${pet.age}</td>`;
        html += `<td>${pet.likes_count}</td>`;
        
        // actions
        html += '<td>';
        if (loggedUser['id'] === pet['id']) { // is owner
            html += `<button class='btn btn-success btn-sm view_pet_btn' onClick="viewPet(${pet.id})">View</button>`
        } else {

        }
        html += '</td>';
        html += '</tr>';
    })

    document.getElementById('pets_list').innerHTML = html;
}

logout = () => {

    setLoggedUser(null);
    fetch(`/api/user/logout`);
    setPage('login');
}

addPet = (e) => {
    e.preventDefault()
    console.log("XX")

}

viewPet = ( petId ) => {

    setPage('view_pet');

    fetch(`/api/pet/${petId}`)
    .then( response => response.json() )
    .then( data => {
        // take list of animals and create HTML
        let html = "";
        data.forEach( pet => {
            html += '<tr>';
            html += `<td>${pet.name}</td>`;
            html += `<td>${pet.type}</td>`;
            html += `<td>${pet.age}</td>`;
            html += `<td>${pet.likes_count}</td>`;

            // actions
            html += '<td>';
            if (loggedUser['id'] === pet.id) { // is owner
                html += `<button class='btn btn-success btn-sm view_pet_btn' onClick="viewPet(${pet.id})">View</button>`
            } else {

            }
            html += '</td>';
            html += '</tr>';
        })

        document.getElementById('pets_list').innerHTML = html;

    } )
    .catch( data => {
        console.log(`error: ${data}`)
    })
}
