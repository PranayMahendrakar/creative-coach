#!/usr/bin/env python3
"""
Simple Creative Writing Coach - Llama-Based Writing Feedback Tool
Provides feedback on creative writing assignments
Author: Pranay M
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
import json

console = Console()

GENRES = ["Fiction", "Poetry", "Creative Non-Fiction", "Flash Fiction", "Short Story",
          "Personal Essay", "Memoir", "Screenplay", "Playwriting", "Children's Literature"]

WRITING_ELEMENTS = ["Character", "Plot", "Setting", "Dialogue", "Theme", 
                    "Voice", "Imagery", "Pacing", "Conflict", "Structure"]


class CreativeWritingCoach:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.submissions = []
    
    def review_writing(self, text: str, genre: str = "Fiction") -> dict:
        prompt = f"""Review this creative writing piece and provide constructive feedback.

Genre: {genre}

Text:
{text}

Return JSON:
{{
    "overview": {{
        "genre": "{genre}",
        "word_count": "approximate",
        "overall_impression": "brief overall assessment",
        "overall_score": 75
    }},
    "strengths": [
        {{
            "element": "what's strong",
            "example": "quote from text",
            "why_effective": "why it works"
        }}
    ],
    "areas_for_improvement": [
        {{
            "element": "what needs work",
            "current_issue": "the problem",
            "suggestion": "how to improve",
            "example_revision": "suggested rewrite"
        }}
    ],
    "craft_analysis": {{
        "voice": {{"score": 75, "feedback": "assessment"}},
        "imagery": {{"score": 70, "feedback": "assessment"}},
        "dialogue": {{"score": 65, "feedback": "assessment"}},
        "pacing": {{"score": 70, "feedback": "assessment"}},
        "structure": {{"score": 80, "feedback": "assessment"}}
    }},
    "memorable_lines": ["lines that stand out positively"],
    "lines_to_revise": [
        {{
            "original": "current line",
            "issue": "what's wrong",
            "suggested": "improved version"
        }}
    ],
    "next_steps": ["prioritized revision tasks"],
    "encouragement": "motivating closing comment"
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        result = self._parse_json(response['message']['content'])
        self.submissions.append({"text": text[:500], "review": result})
        return result
    
    def analyze_element(self, text: str, element: str) -> dict:
        prompt = f"""Analyze the {element} in this creative writing.

Text:
{text}

Element to Analyze: {element}

Return JSON:
{{
    "element": "{element}",
    "analysis": {{
        "current_state": "how it's being used",
        "effectiveness": "how well it works",
        "score": 70
    }},
    "specific_observations": [
        {{
            "observation": "what you notice",
            "example": "from the text",
            "impact": "effect on reader"
        }}
    ],
    "techniques_used": ["writing techniques identified"],
    "missing_opportunities": ["where {element} could be stronger"],
    "improvement_exercises": [
        {{
            "exercise": "practice activity",
            "purpose": "what it develops",
            "instructions": "how to do it"
        }}
    ],
    "mentor_texts": ["published works to study for {element}"],
    "revision_suggestions": ["specific changes to make"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def generate_prompt(self, genre: str, theme: str = "", constraints: str = "") -> dict:
        prompt = f"""Generate a creative writing prompt.

Genre: {genre}
Theme (if specified): {theme}
Constraints (if any): {constraints}

Return JSON:
{{
    "prompt": {{
        "main_prompt": "the writing prompt",
        "genre": "{genre}",
        "suggested_length": "word count range",
        "time_limit": "suggested writing time"
    }},
    "inspiration_elements": {{
        "character_seeds": ["character ideas"],
        "setting_options": ["setting ideas"],
        "conflict_possibilities": ["potential conflicts"],
        "opening_lines": ["possible first lines"]
    }},
    "optional_challenges": [
        {{
            "challenge": "extra constraint",
            "purpose": "what skill it develops"
        }}
    ],
    "mentor_examples": ["published works with similar prompts"],
    "tips_for_this_prompt": ["advice specific to this prompt"],
    "common_pitfalls": ["mistakes to avoid"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def expand_scene(self, scene_summary: str) -> dict:
        prompt = f"""Help expand this scene with more detail and craft.

Scene Summary:
{scene_summary}

Return JSON:
{{
    "original_summary": "{scene_summary}",
    "expanded_elements": {{
        "sensory_details": {{
            "sight": ["visual details to add"],
            "sound": ["audio details"],
            "smell": ["scent details"],
            "touch": ["tactile details"],
            "taste": ["taste details if relevant"]
        }},
        "character_interiority": ["thoughts/feelings to explore"],
        "setting_enrichment": ["environmental details"],
        "dialogue_opportunities": ["conversations to develop"]
    }},
    "expanded_draft": "a more detailed version of the scene",
    "show_dont_tell_opportunities": [
        {{
            "telling": "abstract statement",
            "showing": "concrete scene that shows it"
        }}
    ],
    "pacing_suggestions": {{
        "slow_down": ["moments to linger on"],
        "speed_up": ["moments to compress"]
    }}
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def dialogue_coach(self, dialogue: str, context: str = "") -> dict:
        prompt = f"""Coach me on improving this dialogue.

Context: {context}

Dialogue:
{dialogue}

Return JSON:
{{
    "dialogue_analysis": {{
        "naturalness": {{"score": 70, "assessment": "feedback"}},
        "subtext": {{"score": 65, "assessment": "feedback"}},
        "character_distinction": {{"score": 75, "assessment": "feedback"}},
        "purpose": {{"score": 80, "assessment": "feedback"}}
    }},
    "line_by_line_feedback": [
        {{
            "original_line": "the line",
            "speaker": "who says it",
            "feedback": "what works or doesn't",
            "revision": "improved version"
        }}
    ],
    "subtext_opportunities": ["where to add unspoken meaning"],
    "dialogue_tags": {{
        "overused": ["tags used too much"],
        "suggestions": ["better alternatives"]
    }},
    "revised_dialogue": "improved version of the dialogue",
    "dialogue_exercises": ["practice activities"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def _parse_json(self, content: str) -> dict:
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except:
            pass
        return {"raw_response": content}


def display_menu():
    table = Table(title="✨ Creative Writing Coach", show_header=True)
    table.add_column("Option", style="cyan", width=6)
    table.add_column("Feature", style="green")
    table.add_column("Description", style="white")
    
    table.add_row("1", "Review Writing", "Get full feedback")
    table.add_row("2", "Analyze Element", "Focus on one craft element")
    table.add_row("3", "Generate Prompt", "Get writing prompt")
    table.add_row("4", "Expand Scene", "Develop a scene")
    table.add_row("5", "Dialogue Coach", "Improve dialogue")
    table.add_row("6", "View Elements", "See writing elements")
    table.add_row("0", "Exit", "Close application")
    
    console.print(table)


def main():
    console.print(Panel.fit(
        "[bold blue]✨ Creative Writing Coach[/bold blue]\n"
        "[green]AI-Powered Creative Writing Feedback[/green]\n"
        "[dim]Author: Pranay M[/dim]",
        border_style="blue"
    ))
    
    coach = CreativeWritingCoach()
    
    while True:
        display_menu()
        choice = Prompt.ask("\n[cyan]Select option[/cyan]", default="0")
        
        if choice == "0":
            console.print("[yellow]Goodbye! Keep writing! ✨[/yellow]")
            break
        
        elif choice == "6":
            console.print("\n[bold]Writing Elements:[/bold]")
            for element in WRITING_ELEMENTS:
                console.print(f"  • {element}")
            console.print("\n[bold]Genres:[/bold]")
            for genre in GENRES:
                console.print(f"  • {genre}")
            continue
        
        with console.status("[bold green]Analyzing your writing..."):
            if choice == "1":
                console.print("[dim]Paste your writing (end with 'EOF'):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    lines.append(line)
                genre = Prompt.ask("Genre", default="Fiction")
                result = coach.review_writing("\n".join(lines), genre)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="📖 Writing Review"))
            
            elif choice == "2":
                console.print("[dim]Paste your writing (end with 'EOF'):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    lines.append(line)
                element = Prompt.ask("Element to analyze", default="Voice")
                result = coach.analyze_element("\n".join(lines), element)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title=f"🔍 {element} Analysis"))
            
            elif choice == "3":
                genre = Prompt.ask("Genre", default="Fiction")
                theme = Prompt.ask("Theme (optional)", default="")
                constraints = Prompt.ask("Constraints (optional)", default="")
                result = coach.generate_prompt(genre, theme, constraints)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="💡 Writing Prompt"))
            
            elif choice == "4":
                scene = Prompt.ask("Describe your scene briefly")
                result = coach.expand_scene(scene)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="🎬 Expanded Scene"))
            
            elif choice == "5":
                console.print("[dim]Paste dialogue (end with 'EOF'):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    lines.append(line)
                context = Prompt.ask("Context", default="")
                result = coach.dialogue_coach("\n".join(lines), context)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="💬 Dialogue Feedback"))
        
        console.print("\n" + "="*50)


if __name__ == "__main__":
    main()
