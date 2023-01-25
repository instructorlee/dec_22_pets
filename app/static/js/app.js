/* Events */



startApp = () => {
    setEvents();
    setPage('login');
}

setPage = ( pageID ) => {

    // hide all pages
    document.querySelectorAll('.page')
        .forEach( page => { page.style.display='none' })

    // show selected page
    document.getElementById( pageID ).style.display='flex';
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
                    setPage('dashboard');
                    break;

                default:
                    window.alert('Invalid Login')
            }
        })
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
}


