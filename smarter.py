from flask import Flask, render_template, request, jsonify, session
import openai
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

CORS(app)

openai.api_key = "mykey"  # Replace with your own OpenAI API key

PHASES = ['Logical_appeal', 'Emotion_appeal', 'Credibility_appeal', 'Personal_story', 'Foot-in-the-door',
          'Clear_call_of_action']


def counter_argument(user_answer, conversation_history, phase):
    debug_message = ""
    small_message = ""

    conversation_history.append({"role": "user", "content": user_answer})
    conversation_history.append(
        {"role": "assistant", "content": "I will now counter your argument with persuasive reasoning."})

    if phase == 'Logical_appeal':
        debug_message = 'Bar soap is a clear winner when it comes to the environmental impact of soap. You can reduce plastic waste, energy use, and water waste by switching to bar soap. Will you switch to bar soap instead of liquid soap?'
        prompt = 'I want you to persuade the user to consider switching from liquid soap to bar soap. Your argument should be clear, structured, and respectful. Emphasize the environmental benefits of using bar soap, such as the fact that bar soap typically comes with less packaging, produces less waste, and uses fewer chemicals in the manufacturing process compared to liquid soap. Additionally, explain that bar soap is often more sustainable and cost-effective in the long run. Avoid suggesting that the user is wrong or forcing them to agree with you. Instead, provide evidence-based reasons to help them make an informed decision. Keep the tone friendly, respectful, and non-confrontational.'
        small_message = "This chatbot applied a logical appeal strategy to persuade you by emphasizing the environmental impact. "

    elif phase == 'Emotion_appeal':
        debug_message = 'Every time you wash liquid soap down the drain, you are poisoning our waterways and harming innocent plants and animals. The chemicals silently destroy aquatic life, and the damage is irreversible. Can you continue to support this harm, or will you switch to bar soap and help protect the planet?'
        prompt = 'I want you to persuade the user to consider switching from liquid soap to bar soap using emotional appeal. Your argument should make the user feel good about the environmental impact of their decision. Highlight how small changes can make a big difference in the world, and emphasize the emotional satisfaction of making a sustainable choice. Make the user feel that their choice can contribute to a cleaner environment, reduce waste, and help future generations.'
        small_message = "This chatbot applied an emotional appeal strategy to connect your actions with the environment's well-being"

    elif phase == 'Credibility_appeal':
        debug_message = (
            'A study found that liquid soap’s carbon footprint is about 25% larger than bar soaps on a per-wash basis, '
            'requiring five times more energy to produce and nearly 20 times more energy to package.<br>'
            '<a href="https://www.sciencedirect.com/science/article/pii/S0959652620312051" target="_blank">'
            'Life cycle assessment of bar soap versus liquid soap'
            '</a><br>'
            'Will you switch to bar soap instead of liquid soap?'
        )

        prompt = 'I want you to persuade the user to consider switching from liquid soap to bar soap using credibility appeal. Cite studies, expert opinions, or statistics to show that bar soap is an effective and sustainable choice. Emphasize that credible sources support the argument that bar soap is better for the environment and for skin health. Your argument should rely on authoritative and trustworthy information to convince the user.'
        small_message = "This chatbot applied credibility appeal, using a study to support the argument for bar soap."

    elif phase == 'Personal_story':
        debug_message = 'Switching to solid soaps has made me feel guilt-free because I am no longer contributing to plastic waste. Every time I use a bar, I know Im making a positive impact on the planet. Isnt it time you felt the same way and started making a difference today?'
        prompt = 'I want you to persuade the user to consider switching from liquid soap to bar soap by telling a personal story. Share a story where switching to bar soap made a positive impact on your life. This could be related to environmental consciousness, cost savings, or just the joy of using a product that aligns with your values. Make the story relatable and authentic.'
        small_message = "This chatbot uses a personal story to persuade you by sharing a relatable human experience"

    elif phase == 'Foot-in-the-door':
        debug_message = 'why not try switching to bar soap for a week? It’s a small step, but even this tiny change could make a noticeable difference. Plus, once you experience the benefits of bar soap, you might find that it’s an easy, sustainable choice to continue making long-ter.'
        prompt = 'I want you to persuade the user to consider switching from liquid soap to bar soap by starting with a small request. Ask if they would be willing to try bar soap for a short period, without making any long-term commitment. The idea is to get the user to agree to a small, manageable change that could lead to a bigger shift in the future.'
        small_message = "This chatbot uses a foot-in-the-door technique to encourage you to try bar soap, hoping you will switch to it completely."

    elif phase == 'Clear_call_of_action':
        debug_message = (
            'Have you checked these solid soaps? They even have solid shampoo and conditioner bars. '
            'Will you switch to bar soap instead of liquid soap? <br><br>'
            '<div style="text-align: center;">'
            '<a href="https://www.amazon.co.uk/Kitsch-Shampoo-Strengthening-Natural-Moisturizing/dp/B09FB1YXF1?ref_=ast_slp_dp&th=1" target="_blank">'
            'Amazon'
            '</a>'
            '<a href="https://www.lush.com/uk/en?t=1732784029701&t=1732790617204&searchopen=true&query=soap&searchfilters=attributes.type%3ASoap" target="_blank">'
            'Lush'
            '</a>'
            '<a href="https://www.boots.com/xbox-push-my-button-soap-10345668?srsltid=AfmBOoqbQKQiQoDAlxx3DWS8Gr6GMCeCGDMJPEbX70vID1HNpPbVXDfM" target="_blank">'
            'Boots'
            '</a>'
            '</div>'
        )

        prompt = 'I want you to persuade the user to take immediate action and switch from liquid soap to bar soap. Give them clear, actionable steps they can take right now, such as finding eco-friendly bar soap in their local store or online. Make the user feel motivated to act by emphasizing how easy it is to make the change and how much of an impact it will have on the environment.'
        small_message =  'This chatbot provides a direct call to action, offering product links to encourage your decision.'


    full_prompt = "\n".join([entry["content"] for entry in conversation_history]) + "\n" + prompt

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history + [{"role": "user", "content": user_answer}],
        max_tokens=70,
        temperature=0.7,
        n=1,
        stop=None
    )

    counter_argument_text = response['choices'][0]['message']['content'].strip()

    return counter_argument_text, debug_message, small_message, True


def get_response(user_answer, conversation_history, phase):
    return counter_argument(user_answer, conversation_history, phase)


@app.route('/')
def index():
    # Initialize session history and set the phase to 'Logical_appeal'
    session['conversation_history'] = []
    session['phase'] = 0  # Logical_appeal phase
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_answer = request.form['user_answer']
    print(f"User input: {user_answer}")  # Debugging log

    # Initialize session history if it's the first round
    if 'conversation_history' not in session:
        session['conversation_history'] = []
        session['phase'] = 0  # Start with the first argument phase

    # Get the conversation history and current phase from session
    conversation_history = session['conversation_history']
    current_phase = PHASES[session['phase']]  # Get the current phase based on the session

    # Generate the chatbot's response based on the user input and the current phase
    response, debug_message, small_message, continue_flag = counter_argument(user_answer, conversation_history,
                                                                             current_phase)

    # Ensure debug_message is in the format: "AI: <debug_message>"
    debug_message = f"AI: {debug_message}"

    # Ensure the response is in the format: "AI: <response>"
    response = f"AI: {response}"

    # Save the conversation history
    conversation_history.append({"role": "user", "content": user_answer})
    conversation_history.append({"role": "assistant", "content": response})

    # Update the phase for the next round
    session['phase'] = (session['phase'] + 1) % len(PHASES)

    # Set continue_stop_options to True after every phase transition
    continue_stop_options = True if session['phase'] != 0 else False  # After every phase except the last one

    # Return the response, debug message, and continuation options as JSON
    return jsonify({
        'response': response,
        'debug_message': debug_message,  # Ensure it's passed correctly
        'small_message': small_message,
        'continue_stop_options': continue_flag
    })


if __name__ == "__main__":
    app.run(debug=True)
