% Init

alpha = 0.85;   % Alpha
beta = 0.01;    % Beta
num_samples = 20; % Sampling quantity
delta_time = 1;   % Time interval (1 second)
initial_position = 1.75;  % initial position
initial_velocity = 0;     % initial velocity

% Random generation of measurement data between 1.73 and 1.78,
measurements = 1.73 + (1.78 - 1.73) * rand(1, num_samples);






% Initialize 
filtered_position = zeros(1, num_samples);
filtered_velocity = zeros(1, num_samples);
position = initial_position;
velocity = initial_velocity;

% Alpha-Beta Filter simulation
for i = 1:num_samples
    % Prediction phase: Update location
    position = position + velocity * delta_time;
    % Calculated residual
    residual = measurements(i) - position;
    % Update location and speed
    position = position + alpha * residual;
    velocity = velocity + beta * residual / delta_time;
    % Save the filtered position and speed
    filtered_position(i) = position;
    filtered_velocity(i) = velocity;
end
% Plot result
figure;
hold on;
plot(measurements, 'o--', 'DisplayName', 'Simulated random data', 'Color', [0.5, 0.5, 0.5]);
plot(filtered_position, 'x-', 'DisplayName', ['Alpha = ', num2str(alpha), ', Beta = ', num2str(beta)], 'Color', 'b');
title('Alpha-Beta filter simulation results');
xlabel('Sampling point');
ylabel('position');
legend;
grid on;