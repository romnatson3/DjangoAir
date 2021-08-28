var HEADERS = {'Content-Type': 'application/json',
               'X-Requested-With': 'XMLHttpRequest',
               'X-CSRFToken': get_csrftoken()}


function get_csrftoken (){
    var cookies = document.cookie.split(';')
    var d = {}
    for (var i in cookies) {
        var item = cookies[i].split('=')
        d[item[0].trim()] = item[1]
    }
    return d['csrftoken']
}


function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild)
    }
}


async function sendPriceRequest(value) {
    try {
    var price_url = `${document.location['origin']}/count_total_price/`
    var response = await fetch(price_url, {
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


async function sendDateRequest(value) {
    try {
    var date_url = `${document.location['origin']}/get_flight_date/`
    var response = await fetch(date_url, {
        method: 'POST',
        headers: HEADERS,
        body: JSON.stringify({'destination': value}),
    })
    var result = await response.json()
        if (response.ok) {
            return result
        }
    } catch (error) {
        console.log(error)        
    }
}

async function sendSeatRequest(query) {
    try {
    var seat_url = `${document.location['origin']}/available_seat/`
    var response = await fetch(seat_url, {
        method: 'POST',
        headers: HEADERS,
        body: JSON.stringify(query),
    })
    var result = await response.json()
        if (response.ok) {
            return result
        }
    } catch (error) {
        console.log(error)        
    }
}


async function main() {
    var total_price = document.getElementById('total_price')
    var lunch = document.getElementsByName('lunch')[0]
    var luggage = document.getElementsByName('luggage')[0]
    var seat_class_radio = document.getElementsByName('seat_class')
    var price_data = await sendPriceRequest()
    var seat_class = price_data['seat_class']

    function recount() {
        var price = price_data[seat_class]
        if (lunch.checked) {
            price += price_data['lunch']
        }
        if (luggage.checked) {
            price += price_data['luggage']
        }
        total_price.innerText = `Total price ${price} USD`
    }

    try {
        recount()

        seat_class_radio.forEach((seat) => {
                if (seat.value == seat_class) {
                    seat.checked = true
                }
        })

        seat_class_radio.forEach((seat) => {
            seat.addEventListener('change', (event) => {
                seat_class = event.target.value
                recount()
            })
        })

        lunch.addEventListener('change', (event) => {
            lunch = event.target
            recount()
        })

        luggage.addEventListener('change', (event) => {
            luggage = event.target
            recount()
        })
    } catch (error) {console.log(error)}


    try {
        // Get datetime flight
        var destination = document.getElementsByName('destination')[0]
        destination.addEventListener('input', function(event){
            sendDateRequest(event.target.value).then(data => {
                if (data) {
                    console.log(data)
                    var datalist = document.getElementById('datetime')
                    var input_datetime = document.getElementsByName('datetime')[0]
                    input_datetime.value = ''
                    removeAllChildNodes(datalist)
                    for (var i in data) {
                        var option = document.createElement('option')
                        option.value = data[i]
                        datalist.appendChild(option)
                    }
                }
            })
        })
    } catch (error) {console.log(error)}


    try {
        var datetime = document.getElementsByName('datetime')[0]
        datetime.addEventListener('input', function(event){
            var destination = document.getElementsByName('destination')[0]
            window.localStorage.setItem('datetime', event.target.value)
            window.localStorage.setItem('destination', destination.value)
            console.log(destination.value)
            console.log(event.target.value)
        })
    } catch (error) {console.log(error)}


    try {
        //Get available seat
        seat_class_radio.forEach((seat) => {
            seat.addEventListener('click', function(event){

                var destination = window.localStorage.getItem('destination', destination)
                var datetime = window.localStorage.getItem('datetime', datetime)
                console.log(destination)
                console.log(datetime)
                var seat_class_radio = document.getElementsByName('seat_class')
                var seat_class
                seat_class_radio.forEach((seat) => {
                        if (seat.checked) {
                            seat_class = seat.value
                        }
                })
                var query = {
                    'destination': destination,
                    'datetime': datetime,
                    'seat_class': seat_class,
                }
                sendSeatRequest(query).then(data => {
                    if (data) {
                        console.log(data)
                        var available_seat = document.getElementsByName('available_seat')[0]
                        if (data.length == 0) {
                            available_seat.placeholder = 'No available seat'
                            available_seat.disabled = true
                        } else {
                            available_seat.placeholder = 'Available seats'
                            available_seat.disabled = false
                        }
                        var datalist = document.getElementById('available_seat')
                        available_seat.value = ''
                        removeAllChildNodes(datalist)
                        for (var i in data) {
                            var option = document.createElement('option')
                            option.value = data[i]
                            datalist.appendChild(option)
                        }
                    }
                })
            })
        })
    } catch (error) {console.log(error)}
}

main()
