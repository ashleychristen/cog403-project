import matplotlib.pyplot as plt

features = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
languages = [ 358, 189,
179,
149,
131,
126,
115,
112,
109,
103,
84,
41
]

lang2 = [
    358,
189,
179,
168,
155,
135,
132,
121,
116,
112,
108,
87


]

plt.plot(features, languages)
# plt.plot(features, lang2)
plt.xlabel("Number of Features (per group)")
plt.ylabel("Number of Languages with Data")
plt.title("Meta Trade-Off")
plt.show()