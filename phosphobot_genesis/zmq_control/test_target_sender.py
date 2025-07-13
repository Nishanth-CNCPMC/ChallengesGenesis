from target_sender import handle_target_request

# Define test coordinates
x, y, z = 0.15, 0.0, 0.2
action = "simulate"

print(f"Testing with coordinates: x={x}, y={y}, z={z}, action={action}")
result = handle_target_request(x, y, z, action)

print("Result:")
print(result)

