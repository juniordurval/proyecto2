var socket = io();


socket.on('update data', function(data) {
    var table = document.getElementById('table');

    var row = table.insertRow(-1);

    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);

    cell1.innerHTML = data.Nombre;
    cell2.innerHTML = data.Cuarto;
    cell3.innerHTML = data.Camilla;
    cell4.innerHTML = data.Especialidad;
    cell5.innerHTML = '<button onclick="deleteRow(this, ' + data.ID + ')">REVISAR</button>';
});
/* 
  / \__
 (    @\__ 
 /  JDMV   O
/   (_____/
/_0808/ U
*/

function deleteRow(button, data_id) {
   
    var row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
    socket.emit('delete data', data_id);
}
