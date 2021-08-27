var HEADERS = {'Content-Type': 'application/json',
               'X-Requested-With': 'XMLHttpRequest',
               'X-CSRFToken': get_csrftoken()}

var URL = `${document.location['origin']}/count_total_price/`


function get_csrftoken (){
    var cookies = document.cookie.split(';')
    var d = {}
    for (var i in cookies) {
        var item = cookies[i].split('=')
        d[item[0].trim()] = item[1]
    }
    return d['csrftoken']
}


async function sendRequest(value) {
    try {
    var response = await fetch(URL, {
        method: 'POST',
        headers: HEADERS,
    })
    var result = await response.json()
        if (response.ok) {
            return result
        }
    } catch (error) {
        console.log(error)        
    }
}

var passengers = document.getElementsByName('passengers')[0]
var total_price = document.getElementById('total_price')
var lunch = document.getElementsByName('lunch')[0]
var luggage = document.getElementsByName('luggage')[0]
var seat_class_radio = document.getElementsByName('seat_class')
var seat_class
seat_class_radio.forEach((seat) => {
    if (seat.checked) {
        seat_class = seat.value
    }
})

var price_data = sendRequest().then((data) => {
                    if (data) {
                        return data
                     } 
                 })


function count_total_price(passengers) {
    price_data.then((data) => {
        var price = data[seat_class]
        if (lunch.checked) {
            price += data['lunch']
        }
        if (luggage.checked) {
            price += data['luggage']
        }
        if (passengers) {
            price = price * passengers
        } else {
            price = price * data['passengers']
        }
        total_price.innerText = `Total price ${price} USD`
    })
}

count_total_price()


seat_class_radio.forEach((seat) => {
    seat.addEventListener('change', (event) => {
        seat_class = event.target.value
        count_total_price()
    })
})

lunch.addEventListener('change', (event) => {
    lunch = event.target
    count_total_price()
})

luggage.addEventListener('change', (event) => {
    luggage = event.target
    count_total_price()
})

passengers.addEventListener('change', (event) => {
    passengers = event.target
    if (passengers.value) {
        count_total_price(passengers.value)
    }
})
