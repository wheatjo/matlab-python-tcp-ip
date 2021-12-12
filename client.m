close all;clear;clc;
i=1;
% tcplientUse = tcpclient("127.0.0.1",30000,"Timeout",20);
while i<100
    tcplientUse = tcpclient("127.0.0.1",30000,"Timeout",20);
    pop = double(rand(2048,2048));
    % fopen(tcplientUse);
    disp("connect sucessfully")
    disp("write mat ...")
    
    save('pop.mat', 'pop')

    disp("finish writting !")
    send_flag = 'w'; % means write finish! 
    % config_send = whos('send_data');
    % fwrite(tcpipClient,[config_send.bytes/2;send_data],'float32');
    % fprintf(tcpipClient, send_flag);
    write(tcplientUse,send_flag);
    disp("数据接收")
    recv_data = [];
    pause(1)
    %重复多次接收
    while isempty(recv_data)
        recv_data=read(tcplientUse);
    end
    % 
    
    rec_data = char(recv_data);
    disp(rec_data)
    assert(strcmp(rec_data, 'hru'), 'have get result and error !'); % get result ok
    % fclose(tcplientUse);
    i=i+1;
    clear tcplientUse
end
% clear tcplientUse
