## A Guide to Build NPCs

### Structrues :

- `index` string
  - The unique index of the NPC
- `name` string
  - The name of the NPC in europe style
- `role` string // or career
  - The common role of the NPC in medieval
  - The total types of this field should be about 30 (about 33% of the NPCs)
  - Some of the role types should be unique, ex. King
  - All the available types are in enums/role.txt
- `moods` List[string]
  - The common moods of the NPC
  - Its length of `l` should be 1 <= l <= 3
  - All the available types are in enums/mood.txt
- `interests` List[string]
  - The common interests of the NPC
  - Its length of `l` should be 1 <= l <= 5
  - The total types of this field should be about 20
  - All the available types are in enums/interest.txt
- `playerRelationship` string
  - The relationship from the NPC to the player(assume that there's only one player)
  - Should be integer string
  - Its vale of `val` should be 0 <= val <= 100
- `gender` string
  - The gender of the NPC
  - Should be either male or female
- `personalities` List[string]
  - The personalities of the NPC
  - Its length of `l` should be 1 <= l <= 5
  - The types of this field can be described more details, ex. Materialism
  - The total types of this field should be about 50
  - All the available types are in enums/personality.txt
- `requests` List[string]
  - The specific requests of the NPC(highly related to its role)
  - Its length of `l` should be 0 <= l <= 15
  - The total types of this field should be about 3000 (15% of the total conversations)
  - All the available types are in enums/request.txt

```json
{
  "index": "1",
  "name": "Edric",
  "role": "farmer",
  "moods": ["happy", "hopeful"],
  "interests": ["farming", "gardening", "cooking", "collecting"],
  "playerRelationship": "35",
  "gender": "male",
  "personalities": ["friendly", "loyal", "diligent", "optimistic"],
  "requests": ["Need help with crops"]
},
```

### Evaluate Some Details

- total number : $100\ NPCs$

- total data (conversations) : $20000$

- total lines of codes in dataset.json : $2 + 6 * 20000 = 120002$

- conversation per NPC : $200 (conversations/npc)$

- 假設針對每個 role，將「動詞」×「形容詞」×「名詞」×「條件」做全排列組合，則每個 role 可生成的 requests 數量為：

  - $動詞數 × 形容詞數 × 名詞數 × 條件數$

- 以目前的設計（每個 role 約 8 個動詞、8 個形容詞、8 個名詞、5 個條件）來估算：

  - $8 × 8 × 8 × 5 = 2560\ 個\ requests/role$

- 總共 30 個 role：
  - $2560 × 30 = 76800\ 個\ requests$

> 實際數量會依每個 role 關鍵字數量不同而略有差異，但大致上每個 role 幾千個，總數可達數萬級。

---

**公式：**

$總數 ≈ Σ (動詞數 × 形容詞數 × 名詞數 × 條件數)\ for\ each\ role\ of\ defined\ roles$
