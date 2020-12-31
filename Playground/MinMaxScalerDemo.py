#
#Demo of MinMaxScaler
#
from sklearn.preprocessing import MinMaxScaler
data = [[-1, 2], [-0.5, 6], [0, 10], [1, 18], [1.9, 17]]
scaler = MinMaxScaler()
print(scaler.fit(data))

print("Transform get data max")
print(scaler.data_max_)
print("-------")

print("Transform all data")
print(scaler.transform(data))
print("-------")



print("Transform point")
print(scaler.transform([[2, 2]]))
print("-------")
