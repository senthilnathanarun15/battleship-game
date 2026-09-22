import random

import streamlit as st
from streamlit import session_state, rerun

st.title("battleship")
st.html('''
        <style>
        div[data-testid="stButton"] >button {
        height: 70px;
        width: 100%;
        font-size: 12px;
         background-color:#231FFF ;
         border:1px solid #1FB9FF;
         border-radius:6px;
         
         transition: all 0.25s ease-in-out;
         margin-bottom:8px;
         }
         div[data-testid="stButton"] >button:hover {
         background-color:#FF571F;
         border:2px solid #FFFFFF;
         border-radius:10px;
         box-shadow: 0px 0px 10px rgba(0, 173, 181, 0.5);
         }
         @keyframes hit-fire-pulse{
            0% {transform: scale(1);box-shadow: 0 0 5px #FF3333; filter: brightness(1.0);}
            50% {transform : scale(1.1);box-shadow: 0 0 25px #FF0000; filter: brightness(1.3);}
            100%{transform: scale(1);box-shadow: 0 0 5px #FF3333; filter: brightness(1.0);}
                }
         .hit-animation   {
                background-color: rgba(255, 31, 31, 0.4)!important;
                border : 2px solid #E0D7D7!important;
                color : #FFFFFF !important;
                animation : hit-fire-pulse 1s infinite ease-in-out!important;
                } 
        </style>  
        ''')
if "game_init" not in session_state:
    session_state.game_init = False
def fired_shots (r,c):
    if (r,c) in session_state.ships_coordinates:
        session_state.board[(r,c)] = "Hit"
    else:
        session_state.board[(r,c)] = "Miss"
if not session_state.game_init:
    ship_input = st.number_input('how many ships do you want',min_value=1,max_value=5,value=3)
    ammo_input = st.number_input('how much ammo do you need ',value=10)
    session_state.ships=ship_input
    session_state.ammo_input = ammo_input
    session_state.ships_coordinates= set()
    session_state.board={}
    session_state.ammo_present = True

    if st.button("contineu"):
        session_state.game_init=True
        while len(session_state.ships_coordinates) <session_state.ships:
            r = random.randint(0,4)
            c = random.randint(0,5)
            session_state.ships_coordinates.add((r, c))
        st.rerun()
else:
    hit_count = list(session_state.board.values()).count("Hit")
    total_used_ammo = len(session_state.board)
    ammo = session_state.ammo_input - total_used_ammo
    if ammo <= 0:
        session_state.ammo_present = False
        ammo = 0
    st.write(f"**Ships Destroyed:** {hit_count} / {session_state.ships}")
    left, middle, right = st.columns([0.01, 3, 1.2])
    with middle:
        for r in range(5):
            cols = st.columns(6, gap="medium")
            for c in range(6):
                with cols[c]:
                    coord = (r,c)
                    key = f"btn_{r}_{c}"
                    status=session_state.board.get(coord)
                    if status == "Hit":
                        st.html('''
                                <div class='hit-animation'>
                                <button disabled> 🔥hit </button>
                                </div>
                            ''')
                                
                       # st.button("🔥hit" , key=f"hit_btn_{r}_{c}",disabled=True,use_container_width=True)
                       # st.html("</div>")
                    elif status == "Miss" :
                        st.button("miss", key=f"miss_btn_{r}_{c}", disabled=True, use_container_width=True)

                    else:
                        if session_state.ammo_present :
                            st.button("🎯",
                                    key=key,
                                    on_click=fired_shots,
                                    args = (r,c),
                                    use_container_width = True
                                )
                        if not session_state.ammo_present :
                            st.button("AMMO EMPTY",
                                      key=key,
                                      on_click=fired_shots,
                                      args=(r, c),
                                      use_container_width=True,
                                      disabled= True
                                      )
    with right:

        if session_state.game_init:
            st.metric(f"ammo left:" , value= f"{ammo}/{session_state.ammo_input} ")
        if ammo <= 4 :
            st.error("ammo is very low")
        if ammo <= 0 :
            ammo = 0
            st.error("you have no ammo")
        if hit_count == session_state.ships :
            st.balloons()
            st.success("you have won the game ")
            ammo = 0 

        if st.button("restart game"):
            session_state.game_init = False
            st.rerun()