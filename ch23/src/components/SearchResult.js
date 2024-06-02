import React, { useState, useEffect } from 'react';
import axios from 'axios';
import naver from '../images/btnG_아이콘사각.png';
import { useNavigate } from 'react-router-dom';

const SearchResult = (props) => {
    const { label } = props;
    const [flowerInfo, setFlowerInfo] = useState(null);
    const navigate = useNavigate();

    const goShoppingPage = () =>{
        navigate(`/naverShopping/${flowerInfo.flowername_kr}`)
    };
    useEffect(() => {
        const fetchFlowerInfo = async () => {
            try {
                const response =await axios.get(`https://fdy-backend-server-jwan.onrender.com/flowers?flowername=${label}`);
                setFlowerInfo(response.data);
            } catch(error) {
                console.error('Error searching for flower:',error);
                setFlowerInfo(null);
            }
        };
        fetchFlowerInfo();
    }, [label]);

    return (
        <div>
            {flowerInfo &&(
            <div style={{backgroundColor: 'white',padding: '10px', borderRadius: '8px',display:'flex',
            flexDirection: 'column'}}> 
                <h2 style={{ color: 'darkgreen', fontSize:'20px',alignSelf:'flex-start',marginBottom:'10px'}}>
                    <span style={{borderBottom: `3px solid darkgreen`,paddingBottom: '2px'}}>
                        {flowerInfo.flowername_kr}
                    </span>
                </h2>
                <table style={{ borderSpacing:'10px', wordBreak: 'keep-all'}}>
                    <tbody>
                        <tr>
                            <td style={{color:'black',width:'15%'}}><strong>이름</strong></td>
                            <td style={{color:'black',width:'85%'}}>{flowerInfo.flowername}</td>
                        </tr>
                        <tr>
                            <td style={{color:'black',width:'15%'}}><strong>서식지</strong></td>
                            <td style={{color:'black',width:'85%'}}>{flowerInfo.habitat}</td>
                        </tr>
                        <tr>
                            <td style={{color:'black',width:'15%'}}><strong>학명</strong></td>
                            <td style={{color:'black',width:'85%'}}>{flowerInfo.binomialName}</td>
                        </tr>
                        <tr>
                            <td style={{color:'black',width:'15%'}}><strong>분류</strong></td>
                            <td style={{color:'black',width:'85%'}}>{flowerInfo.classification}</td>
                        </tr>
                        <tr>
                            <td style={{color:'black',width:'15%'}}><strong>판매검색</strong></td>
                            <td style={{color:'black',width:'85%'}}>
                                <button onClick={goShoppingPage} style={{backgroundColor: '#03c75A',
                                    display:'flex',justifyContent:'center',textAlign:'center',border:'none'
                                }}>
                                    <img src={naver} style={{marginRight: '5px'}} width="20" height="20" alt='네이버 로고'/>네이버 쇼핑
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>    
            </div>
            )}
        </div>
    )
}

export default SearchResult;