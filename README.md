results = np.array([dado1.jogar_dado(2**i) for i in range(15)])

# Plot the histogram
fig, ax = plt.subplots()
ax.bar(np.arange(1, dado1.faces + 1) - 0.2, results.T, width=0.4, align='center', alpha=0.5)
ax.set_xlabel('Face')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of Dice Rolls')
ax.set_xticks(np.arange(1, dado1.faces + 1))
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
