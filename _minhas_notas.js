const VPL_Node = require("./vpl/VPL_Node");

        // liga a lampada
        client_lampada.write('{"id":1, "method":"set_power","params":["on", "smooth", 100]}\r\n');
        // luz branca
        client_lampada.write('{"id":1,"method":"set_rgb","params":[16777215, "smooth", 1000]}\r\n');

        // luz azul
		    client_lampada.write('{"id":1,"method":"set_rgb","params":[13311, "smooth", 1000]}\r\n');

        // luz vermelha
        client_lampada.write('{"id":1,"method":"set_rgb","params":[16711680, "smooth", 1000]}\r\n');
        
// luz amarela
client_lampada.write('{"id":1,"method":"set_rgb","params":[16774912, "smooth", 1000]}\r\n');

Formas para a VPL

Square
Diamond
TriangleDown
TriangleUp
TriangleLeft
TriangleRight
Circle
RoundedRectangle
