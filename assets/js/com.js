window.onload = () => {

    // 加载滚动注释
    bioUpdate();

}

function bioUpdate() {
    const text = document.querySelector('.bio-text');

    // 文本
    const contentArray = ["ForcecatDevsAPIs", "力猫开发社团API合集", "哇哇哇，阿巴阿巴阿巴"];
    let index = 0;

    // 颜文字
    const emotionArray = ["(*/ω＼*)", "( •̀ ω •́ )y", "( •̀ .̫ •́ )✧", "ヽ(＊>∇<)ﾉ", "ฅ"];
    let eIndex = 0;

    // 变向
    let change = true;

    // 拼接字符串
    let i = 0;
    let tempStr = contentArray[0] + "  " + emotionArray[0];

    setInterval(() => {

        if (change) {
            text.innerHTML = tempStr.slice(0, ++i);
        } else {
            if (i <= 0) {
                text.innerHTML = "_";
                i--;
            } else {
                text.innerHTML = tempStr.slice(0, i--);
            }
        }

        if (i === tempStr.length + 10) {
            change = false;
        } else if (i < 0) {
            i = 0;
            change = true;
            index++;
            if (index >= contentArray.length) {
                text.innerHTML = "_";
                index = 0;
            }
            eIndex++;
            if (eIndex >= emotionArray.length) {
                eIndex = 0;
            }
            tempStr = contentArray[index] + "  " + emotionArray[eIndex];
        }

    }, 100)
}
