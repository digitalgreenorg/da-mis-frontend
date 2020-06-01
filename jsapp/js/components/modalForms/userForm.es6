import React from 'react';
import TextBox from 'js/components/textBox';
import {bem} from 'js/bem';
import {t} from 'js/utils';
import UserAssetPermsEditor from '../permissions/userAssetPermsEditor.es6';

class UserForm extends React.Component {

  saveUser(){

  }

  render(){
    return(
      <bem.FormModal__form className='userForm'>
        <bem.FormModal__item>
          <TextBox
          label={t('Username')}
          />
        </bem.FormModal__item>
        <bem.FormModal__item>
        <TextBox
                  label={t('Name')}
                  // errors={this.state.fieldsErrors.name}
                  // value={this.state.name}
                  // onChange={this.nameChange}
                  // description={t('Use this to display your real name to other users')}
                />
        </bem.FormModal__item>
        <bem.FormModal__item>
          <TextBox
          type='password'
          label={t('Password')}
          />
        </bem.FormModal__item>
        <bem.FormModal__item>
          <TextBox
          type='email'
          label={t('Email')}
          />
        </bem.FormModal__item>
        {/* <UserAssetPermsEditor 
          username='super_admin'
          uid={uid}
          assignablePerms={this.state.assignablePerms}  
          nonOwnerPerms={this.state.nonOwnerPerms}
          onSubmitEnd={this.onPermissionsEditorSubmitEnd}
        /> */}
        <bem.Modal__footer>
          <bem.Modal__footerButton
            m='primary'
            type='submit'
            onClick={this.saveUser}
          >
            {t('Add User')}
          </bem.Modal__footerButton>
        </bem.Modal__footer>
      </bem.FormModal__form>
    );
  }
}

export default UserForm;
