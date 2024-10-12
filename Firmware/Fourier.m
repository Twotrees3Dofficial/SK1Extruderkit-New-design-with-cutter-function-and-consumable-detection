filePath = fullfile(getenv('USERPROFILE'), 'Desktop', 'Excel.xlsx'); % Import table data
x = xlsread(filePath, 'Sheet1', 'A1:A20');  
y = xlsread(filePath, 'Sheet1', 'B1:B20');  
f = fit(x, y, 'fourier2');  % Replacement filter model



figure;
hold on;


plot(f ,'-');  
disp(f);
plot(x, y, 'o', 'DisplayName', 'Raw data', 'Color', [0.5, 0.5, 0.5]);

% Copy the parameters here
       a0 =      1.301  ;
       a1 =      0.9384 ;
       b1 =      0.4135 ;
       a2 =     -0.4723;
       b2 =     -0.07153;
       w =         7.406 ;


x = linspace(0, 1.0, 1000); 
y=  a0 + a1*cos(x*w) + b1*sin(x*w) + a2*cos(2*x*w) + b2*sin(2*x*w)

%y=  1.301 + 0.9384 *cos(x*7.406) + 0.4135*sin(x*7.406) -0.4723*cos(14.812*x) -0.07153*sin(14.812*x)



plot(x, y,  '--', 'DisplayName','Fitting curve','Color', 'b');  


xlabel('Measured value');
ylabel('Actual value');
legend('show');
title('Quadratic Fourier fitting graph');
grid on;