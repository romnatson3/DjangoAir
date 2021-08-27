var HEADERS = {'Content-Type': 'application/json',
               'X-Requested-With': 'XMLHttpRequest',
               'X-CSRFToken': get_csrftoken()}

var URL = `${document.location['origin']}/get_flight_date/`

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


function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}


var destination = document.getElementsByName('destination')[0]
destination.addEventListener('input', function(event){
    sendRequest(event.target.value).then(data => {
        if (data) {
            console.log(data)
            var datetime = document.getElementById('datetime')
            var input_datetime = document.getElementsByName('datetime')[0]
            input_datetime.value = ''
            removeAllChildNodes(datetime)
            for (var i in data) {
                var option = document.createElement('option')
                option.value = data[i]
                datetime.appendChild(option)
            }
        }
    })
})

