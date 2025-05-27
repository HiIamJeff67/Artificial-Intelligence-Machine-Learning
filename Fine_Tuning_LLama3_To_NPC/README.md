# 微調 LLama3 8B 模型用於在遊戲中 NPC 使其產生人性化對話

## 透過 API 以及 Python 函式製作大量 Dataset

- 構想架構跟主題
  - 為了使其更符合遊戲當下情境，且讓對話基於某些特定條件，設計出以下框架作為微調 LLama3 所使用的資料為主：
    - 其中，player_input 欄位儲存玩家的輸入，假設為單人遊戲。
    - npc_informations 欄位存放有關 npc 的各項數據。
    - environment_informations 欄位存放有關環境（除了對話雙方以外的其他因素，可在擴增）的各項數據。
    - npc_output 欄位為模型作為一位 npc 判斷這樣的資料後應該產生的輸出。
    - 以下 json 內的一筆資料稱為一個 conversation (對話)。

```json
{
    "player_input": "",
    "npc_informations": {
      "index": "",
      "name": "",
      "role": "",
      "moods": [],
      "interests": [],
      "playerRelationship": "",
      "gender": "",
      "personalities": [],
      "requests": []
    },
    "environment_informations": {
      "index": "",
      "weather": "",
      "time": ""
    },
    "npc_output": ""
  },
```

- 之所以要有這樣的資料設計，是設想每個 NPC 可能依照微調時給定的 dataset 使其產生更符合特定遊戲的 NPC 該有的回覆，意即針對每個遊戲可以透過給定不同微調的 dataset 而使得微調後的 LLama3 更符合遊戲內 NPC 的答覆，且產生非確定性、具有一定特色的對話。

- 透過先跟 AI 對話產生 npc_informations 中各欄位事先設定好的 enum 值（產生之結果存在 `/enums/@generated` 底下），並透過 `txt_to_list.py` 處理，將純文字轉換成 Python List 的結構，以便日後產生 dataset 時使用。同理處理 environment_informations

- 之後透過對於特定職業（角色），產生可能的任務，由於每個職業任務可能會有多個任務，且期望會有大約 3000 筆任務，因此此部分的生成採用組合的方式：

  1. 先產生動詞、形容詞、名詞以及條件子句
  2. 透過「動詞」＋「形容詞」＋「名詞」＋「條件子句」的方式組合成完整句子
  3. 其中數量大約為每個職業（共計 30 個）具有：
     - 動詞：大約 8 個
     - 形容詞：大約 8 個
     - 名詞：大約 8 個
     - 條件子句：大約 5 個
  4. 因此大約會有 $8 \cdot 8 \cdot 8 \cdot 5 = 2560\ (個任務/NPC)$，相當於會有 $2560 \cdot 30 = 76800\ (個任務)$
  5. 此部分透過 `util/combine_keywords_to_sentences()` 完成，且傳入參數去限制每個 NPC 生成的任務最多 100 個，故此資料會有總計 3000 個任務。

- 最後在合併 npc_informations 和 environment_informations 以及透過 OpenRouter 上更強大的模型(LLama3.3 70B)的 API 去生成對應 npc_informations 和 environemnt_informations 該有的 player_input 跟 npc_output，**總計產生大約 20000 筆對話**。（任務佔全部對話大約 30% 的比例）

## 使用產生之 dataset 微調 LLama 3.3 8B 模型
