//Email Seneca, 
let map, searchManager;
let BingMapsKey = 'AuV6Kc6hF3yFNL_DXFTDGuSu9DCdIK8zYF208z0eNdqbXtt87UHslIKJ70900Wbj';
let data = ""//String to store data that will be saved 
let userLat , userLong, updatedLat, updatedLong//Coords variables
let used = []//Array for posted numbers
let lats = []
let longs = []
let words = ["barber", "massage", "nails", "repair", "computer", "car"]
let counter = 1
let range = 30//Range of loops

function GetMap() {
    map = new Microsoft.Maps.Map('#myMap', {
        credentials: BingMapsKey
    });

    //Load the spatial math module
    Microsoft.Maps.loadModule("Microsoft.Maps.SpatialMath", function () {
        //Request the user's location
        navigator.geolocation.getCurrentPosition(function (position) {
            let loc = new Microsoft.Maps.Location(position.coords.latitude, position.coords.longitude);
            userLat = position.coords.latitude
            userLong = position.coords.longitude
            updatedLat = userLat + 0.005
            updatedLong = userLong + 0.005
            //Save first coordinates of the user
            OGLat = userLat
            OGLong = userLong
            OGUPLat = updatedLat
            OGUPLong = updatedLong
            //Create an accuracy circle
            let path = Microsoft.Maps.SpatialMath.getRegularPolygon(loc, position.coords.accuracy, 36, Microsoft.Maps.SpatialMath.Meters);
            let poly = new Microsoft.Maps.Polygon(path);
            map.entities.push(poly);

            //Add a pushpin at the user's location.
            let pin = new Microsoft.Maps.Pushpin(loc);
            map.entities.push(pin);

            //Center the map on the user's location.
            map.setView({ center: loc, zoom: 17 });
        });
    });
}



function geocode() {
    function Request(query){
        //Move around the map and get locations from specific square
        userLat = OGLat
        userLong = OGLong
        updatedLat = OGUPLat
        updatedLong = OGUPLong
        for (let x = 0; x < range; x++){
            const longlat = [userLat, userLong, updatedLat, updatedLong]
            var geocodeRequest = "http://dev.virtualearth.net/REST/v1/LocalSearch/?query=" + encodeURIComponent(query) + "&userMapView=" + encodeURIComponent(longlat) + "&maxResults=25&jsonp=GeocodeCallback&key=" + BingMapsKey;
            CallRestService(geocodeRequest, GeocodeCallback);
            userLat += 0.005
            userLong += 0.005
            updatedLat += 0.005
            updatedLong += 0.005
        }
        console.log(used)
    }
    document.getElementById('output').innerHTML = "" // Clear out old input before posting new search result
    let input = document.getElementById('input').value;
    let query
    //Check if input is empty, and if it is search all the themes, otherwise search for specific request
    if (input.length == 0 ){
        for (let z = 0; z < words.length; z++) {
            query = words[z]
            Request(query)
        }
    } else {
        query = input
        Request(query)
    }
}

function GeocodeCallback(response) {
    let output = document.getElementById('output');
    //Chech if phone number has been already posted
    function HasDuplicate(object){
        for (let i = 0; i < used.length; i++){
            if(used[i] == object)
            {
                return true
            }
        }
        return false
    }

    if (response &&
        response.resourceSets &&
        response.resourceSets.length > 0 &&
        response.resourceSets[0].resources) {

        var results = response.resourceSets[0].resources;

        let html = ['<table>'];
       
        for (var i = 0; i < results.length; i++) {
            if (!HasDuplicate(results[i].PhoneNumber)){
                html.push('<tr><td>' + counter + " " + '</td><td>' + results[i].name + '</td><td>' + results[i].PhoneNumber + '</td></tr>');//<td>', results[i].Website, '</td>
                data += results[i].PhoneNumber + " , " + results[i].name + "\n"//Save Data into file
                //PROBLEMS
                lats.push(results[i].latitude)//Save latitude and longtitude so we can put a push pin on the map
                longs.push(results[i].longitude)
                console.log("Latitude: " + results[i].latitude + " Longtitude: " + results[i].longitude)
                //PROBLEMS
                used.push(results[i].PhoneNumber)
                counter++
            } else {
                console.log("IsDuplicate " + results[i].name)
            }
        }
       

        html.push('</table>');
        


        output.innerHTML += html.join('');


    } else {
        output.innerHTML = "No results found.";
    }
}

let WriteToFile = () => {

    // Convert the text to BLOB.
    const textToBLOB = new Blob([data], { type: 'text/plain' });
    const sFileName = 'formData.txt';	   // The file to save the data.

    let newLink = document.createElement("a");
    newLink.download = sFileName;

    if (window.webkitURL != null) {
        newLink.href = window.webkitURL.createObjectURL(textToBLOB);
    }
    else {
        newLink.href = window.URL.createObjectURL(textToBLOB);
        newLink.style.display = "none";
        document.body.appendChild(newLink);
    }

    newLink.click(); 
}

function CallRestService(request) {
    var script = document.createElement("script");
    script.setAttribute("type", "text/javascript");
    script.setAttribute("src", request);
    document.body.appendChild(script);
}
