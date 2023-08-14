import matplotlib.pyplot as plt

def plot_single_threshold(df, N_SAMPLES, label=' '):
    plt.figure(dpi=100)
    # 標準偏差で幅をつけて薄くプロット
    plt.fill_between(
        df.index,
        y1=df['return_rate']-df['std'],
        y2=df['return_rate']+df['std'],
        alpha=0.3
        )
    # 回収率を実線でプロット
    plt.plot(df.index, df['return_rate'], label=label)
    # labelで設定した凡例を表示させる
    plt.legend()
    # グリッドをつける
    plt.grid(True)
    plt.xlabel('threshold')
    plt.ylabel('return_rate')
    plt.show()
