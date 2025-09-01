# MacroQuest 🍽️

MacroQuest is a smart, personal nutrition tracker designed to help users log daily meals, monitor macronutrient intake (calories, protein, fats, carbs), and stay consistent with their health goals.

It makes tracking fast and rewarding by learning from your habits: previously added meals and ingredients are saved for quick future entries.

---

## ✨ Features

- 🚀 **Fast Logging**: Save common foods and meals to speed up daily tracking.
- 🏆 **Daily Goals & Streaks**: Track if you met your macronutrient goals each day and build streaks.
- 📈 **Progress Dashboard**: Review your nutrition history and patterns over time.
- 🧠 **Future Plan**: Smart meal suggestions based on your eating patterns.
- 📄 **Local Logs**: All data stored locally in SQLite (`macroquest.db`) for privacy and performance.
- 🌟 **Expandable**: Easily extend with badges, reminders, charts.

---

## 📦 Installation

```bash
git clone https://github.com/yourname/macroquest.git
cd macroquest
pip install -r requirements.txt
```

### Show Meals for a Specific Date

You can view all meals logged on a specific date using the `--date` option:

```bash
python -m macroquest.cli.meal_tracking --date 2025-09-01
```
