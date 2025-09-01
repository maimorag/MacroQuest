# MacroQuest 🍽️

_A personal nutrition tracker with smart meal logging and macronutrient insights._

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

## 🌟 About

MacroQuest is a CLI-based nutrition tracker designed to help users log meals, calculate consumed macronutrients (calories, protein, fat, carbohydrates), and compare them against daily goals.  
It keeps a local history in SQLite and supports both **interactive entry** and **JSON/Excel input**.

---

## ✨ Features

- 🚀 **Fast Logging**: Enter meals via JSON, Excel, or interactively.
- 🏆 **Daily Goals**: Track calories, protein, fats, and carbs.
- 📈 **History Tracking**: Query your nutrition log by date or show daily totals.
- 💾 **SQLite Database**: Meals are stored locally (`macroquest.db`) for privacy.
- 📄 **Excel Export**: Save summaries as `nutrition_summary.xlsx`.
- 🔧 **Extensible**: Modular design with `services`, `utils`, `db`.

---

## 📦 Installation

```bash
git clone https://github.com/yourname/macroquest.git
cd macroquest
pip install -r requirements.txt
```

## ⚡ Usage

#### Run MacroQuest directly as a Python module

```bash
python -m macroquest.cli.meal_tracking [options]
```

#### Track today’s meals vs. goals

```bash
python -m macroquest.cli.meal_tracking -g examples/nutritions_goals.json -m examples/meals.json
```

#### Show meal history (all entries in the database)

```bash
python -m macroquest.cli.meal_tracking --history
```

#### Show daily aggregated nutrition totals

```bash
python -m macroquest.cli.meal_tracking --history --daily
```

#### Show meals for a specific date

```bash
python -m macroquest.cli.meal_tracking --date 2025-09-01
```

#### Skip saving meals to the database (for testing purposes)

```bash
python -m macroquest.cli.meal_tracking -g examples/nutritions_goals.json -m examples/meals.json --skip-db
```

#### Export results to Excel

```bash
python -m macroquest.cli.meal_tracking -g examples/nutritions_goals.json -m examples/meals.json --create-excel
```

### Example Output

```bash
=== Nutrition Summary ===
Consumed:
{
  "calories": 542.81,
  "protein": 39.18,
  "fat": 17.01,
  "carbohydrates": 57.57
}
Remaining:
{
  "calories": 1457.19,
  "protein": 110.82,
  "fat": 52.99,
  "carbohydrates": 192.43
}
```

## 🔮 Future Improvements

Web dashboard with charts.

Streaks & achievements.

Barcode scanner for quick food logging.

API integration with fitness apps.

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](macroquest\LICENSE) file for details.
