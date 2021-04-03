        // liga a lampada
        client_lampada.write('{"id":1, "method":"set_power","params":["on", "smooth", 100]}\r\n');
        // luz branca
        client_lampada.write('{"id":1,"method":"set_rgb","params":[16777215, "smooth", 1000]}\r\n');