function call_click() {
    fetch('call_click', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }

        if (response.is_levelup) { 
            get_boosts() 
        }
        return Promise.reject(response)
    }).then(data => {
        document.getElementById('coins').innerText = data.core.coins
    }).catch(error => console.log(error))
}

function get_boosts() { 
    fetch('boosts', { 
        method: 'GET' 
    }).then(response => { 
        if (response.ok) { 
            return response.json() 
        }  
        return Promise.reject(response) 
    }).then(boosts => { 
        const panel = document.getElementById('boosts-holder') 
        panel.innerHTML = ''
        boosts.forEach(boost => { 
            add_boost(panel, boost) 
        }) 
    }).catch(error => console.log(error)) 
}

function add_boost(parent, boost) { 
    const button = document.createElement('button') 
    button.setAttribute('class', 'boost') 
    button.setAttribute('id', `boost_${boost.id}`) 
    button.setAttribute('onclick', `buy_boost(${boost.id})`) 
    button.innerHTML = ` 
        <p>lvl: <span id="boost_level">${boost.level}</span></p>
        <p>+<span id="boost_power">${boost.power}</span></p> 
        <p><span id="boost_price">${boost.price}</span></p> 
    ` 
    parent.appendChild(button) 
}


// function buy_boost(boost_id) {
//     fetch('buy_boost/' + boost_id, {
//         method: 'GET'
//     }).then(response => {
//         if (response.ok) {
//             return response.json()
//         }
//         return Promise.reject(response)
//     }).then(data => {
//         document.getElementById('coins').innerText = data.coins
//     }).catch(error => console.log(error))
// } 

function getCookie(name) { 
    let cookieValue = null; 
    if (document.cookie && document.cookie !== '') { 
        const cookies = document.cookie.split(';'); 
        for (let i = 0; i < cookies.length; i++) { 
            const cookie = cookies[i].trim(); 
            if (cookie.substring(0, name.length + 1) === (name + '=')) { 
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); 
                break; 
            } 
        } 
    } 
    return cookieValue; 
}

function buy_boost(boost_id) {
    const csrftoken = getCookie('csrftoken') 

    fetch(`boost/${boost_id}/`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrftoken, 
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) return response.json()
        else return Promise.reject(response)
    }).then(response => {
        if (response.error) return
        const old_boost_stats = response.old_boost_stats
        const new_boost_stats = response.new_boost_stats
       
        const coinsElement = document.getElementById('coins')
        coinsElement.innerText = Number(coinsElement.innerText) - old_boost_stats.price
        const powerElement = document.getElementById('click_power')
        powerElement.innerText = Number(powerElement.innerText) + old_boost_stats.power

        update_boost(new_boost_stats) 
    }).catch(err => console.log(err))
}

function update_boost(boost) {
    const boost_node = document.getElementById(`boost_${boost.id}`)
    boost_node.querySelector('#boost_level').innerText = boost.level
    boost_node.querySelector('#boost_power').innerText = boost.power
    boost_node.querySelector('#boost_price').innerText = boost.price
}