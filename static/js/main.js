// initialize global variables.
var edges;
var nodes;
var network;
var container;
var options, data;
var is_hidden = false

var wiki_endpoint = "https://en.wikipedia.org/api/rest_v1/page/summary/"

function parse_data(data) {
    nodes = []
    edges = []
    nn = data["Nodes"]
    ee = data["Edges"]

    for (var i = 0; i < nn.length; i++) {
        if(i==0){
            nodes[0] = { "id": nn[i], "label": nn[i], "shape": "dot", "size": 10, "hidden":false}
        } else{
            var n = { "id": nn[i], "label": nn[i], "shape": "dot", "size": 10,  "hidden":false }
            nodes[i] = n
        }
    }

    for (var i = 0; i < ee.length; i++) {
        var e = { "id": i, "from": ee[i]["from"], "to":ee[i]["to"],"hidden":false}
        edges[i] = e
    }


    return [nodes, edges]
}

function get_edges(network, node,nodes){
    children_nodes = network.getConnectedNodes(node["id"],'from')
    children_edges = network.getConnectedEdges(node["id"])

    console.log(children_edges)
//    console.log(nodes.get(node["id"]))
//    console.log(nodes.get("Donkey"))

//    Show nodes
if(is_hidden){
    is_hidden = false
    for(var i=0; i<children_nodes.length; i++){
        nid = children_nodes[i]
        eid = children_edges[i]

        network.body.data.nodes.update([{"id": nid, "hidden":is_hidden}])
        network.body.data.edges.update([{"id": eid, "hidden":is_hidden}])
       }
    }else{
    is_hidden = false
        for(var i=0; i<children_nodes.length; i++){
         nid = children_nodes[i]
        eid = children_edges[i]

        network.body.data.nodes.update([{"id": nid, "hidden":is_hidden}])
        network.body.data.edges.update([{"id": eid, "hidden":is_hidden}])
       }
    }
}

// This method is responsible for drawing the graph, returns the drawn network
function drawGraph(nodes, edges) {

    var container = document.getElementById('mynetwork');

    nodes = new vis.DataSet(nodes)
    edges = new vis.DataSet(edges)

    data = { nodes: nodes, edges: edges };

    var options = {
        "autoResize":true,
        "configure": {
            "enabled": false,
        },
        "edges": {
            "color": {
                "inherit": true
            },
            "smooth": {
                "enabled": false,
                "type": "continuous"
            }
        },
        "interaction": {
            "dragNodes": true,
            "hideEdgesOnDrag": false,
            "hideNodesOnDrag": false,
            "navigationButtons": false,
            "selectable": true,
            "hover":true
        },
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "fit": true,
                "iterations": 1000,
                "onlyDynamicEdges": false,
                "updateInterval": 50
            }
        }
    };

    network = new vis.Network(container, data, options);
    network.on( 'click', function(properties) {

    var ids = properties.nodes;
    var clickedNodes = nodes.get(ids);
     if(clickedNodes[0]["label"]){
//            alert(clickedNodes[0]["label"])
            document.getElementById("node_title").innerHTML = clickedNodes[0]["label"]
            document.getElementById("node_data").innerHTML = "<p style='text-align:center'>Loading</p>"

        get_edges(network, clickedNodes[0],data.nodes)



//            -----------------------------------------------------------------------------------
     let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {

            if (xhr.readyState === 4) {
                response = xhr.responseText;
                response = JSON.parse(response)

                if (response["extract"]){
                    document.getElementById("node_data").innerHTML = "<p style='text-align:justify'>"+response["extract"]+"</p>"
                }else{
                    document.getElementById("node_data").innerHTML = "<p style='text-align:justify'>Error loading data</p>"
                }
//                    alert()

      }
    }
//    xhr.open("GET", "/ask_wiki/"+clickedNodes[0]["label"],true);
    xhr.open("GET", wiki_endpoint+clickedNodes[0]["label"].replace(/\s+/g, '_'),true);
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.send();
//            -----------------------------------------------------------------------------------
        }

});

    return network;

}

function hide_element_login(){
    student_id_login_div = document.getElementById('student_id_login_div')
    student_id_login = document.getElementById('student_id_login')
    username_login_div = document.getElementById('username_login_div')
    username_login = document.getElementById('username_login')

    if(document.getElementById('is_teacher_login').checked){
        student_id_login_div.style.visibility = 'hidden'
        student_id_login.required = false
        username_login_div.style.visibility = 'visible'
        username_login.required = true
    }else{
        student_id_login_div.style.visibility = 'visible'
        student_id_login.required = true
        username_login_div.style.visibility = 'hidden'
        username_login.required = false
    }
}

function hide_element_register(){
     student_id_div = document.getElementById('student_id_div')
     student_id = document.getElementById('student_id')
     student_id_label = document.getElementById("student_id_label")
     username = document.getElementById("username")
     username_div = document.getElementById("username_div")
     username_label = document.getElementById("username_label")

    if(document.getElementById('is_teacher').checked){
        student_id_div.style.visibility = 'hidden'
        student_id.required = false
        student_id_label.style.visibility = 'hidden'
        username_div.style.visibility = 'visible'
        username.required = true
    }else{
        student_id_div.style.visibility = 'visible'
        student_id.required = true
        username_div.style.visibility = 'hidden'
        username_label.style.visibility = 'hidden'
        username.required = false
   }
}

function hide_element(id){
    el = document.getElementById(id)
    if(el.style.visibility == 'hidden'){
        el.style.visibility = 'visible'
    }
    else{
        el.style.visibility == 'hidden'
    }
}