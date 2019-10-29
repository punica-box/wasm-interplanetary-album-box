#![cfg_attr(not(feature = "mock"), no_std)]
#![feature(proc_macro_hygiene)]
extern crate ontio_std as ostd;
use ostd::abi::{EventBuilder, Sink, Source};
use ostd::database;
use ostd::prelude::*;
use ostd::runtime;
use ostd::abi::{Encoder,Decoder};

const ITEM_PREFIX: &str = "ITEM";

#[derive(Encoder, Decoder)]
struct Info {
    encrypted_ipfs_hash: String,
    ext: String,
    aes_iv: String,
    encode_g_tilde: String,
}

fn is_item_exist(encrypted_ipfs_hash: &str, info: &[Info]) -> bool {
    for i in info.iter() {
        if i.encrypted_ipfs_hash.as_str() == encrypted_ipfs_hash {
            return true;
        }
    }
    false
}

fn put_one_item(
    ont_id: &Address,
    encrypted_ipfs_hash: &str,
    ext: &str,
    aes_iv: &str,
    encode_g_tilde: &str,
) -> bool {
    assert!(runtime::check_witness(ont_id));
    let item_key = [ITEM_PREFIX.as_bytes(), ont_id.as_ref()].concat();
    let mut item_list_info: Vec<Info> = database::get(&item_key).unwrap_or(Vec::<Info>::new());
    if is_item_exist(encrypted_ipfs_hash, &item_list_info) {
        EventBuilder::new()
            .string("PutFail")
            .string(encrypted_ipfs_hash)
            .notify();
        return false;
    }
    let item = Info {
        encrypted_ipfs_hash: encrypted_ipfs_hash.to_string(),
        ext: ext.to_string(),
        aes_iv: aes_iv.to_string(),
        encode_g_tilde: encode_g_tilde.to_string(),
    };
    item_list_info.push(item);
    database::put(item_key, item_list_info);
    EventBuilder::new()
        .string("Put")
        .string(encrypted_ipfs_hash)
        .notify();
    true
}

fn get_item_list(ont_id: &Address) -> Vec<Info> {
    let item_key = [ITEM_PREFIX.as_bytes(), ont_id.as_ref()].concat();
    return database::get(item_key).unwrap_or(Vec::<Info>::new());
}

fn del_ont_item(ont_id: &Address, ipfs_hash: &str) -> bool {
    assert!(runtime::check_witness(ont_id));
    let item_key = [ITEM_PREFIX.as_bytes(), ont_id.as_ref()].concat();
    let mut item_list: Vec<Info> = database::get(&item_key).unwrap_or(Vec::<Info>::new());

    let index = item_list
        .iter().position(|x|x.encrypted_ipfs_hash.as_str() == ipfs_hash).unwrap_or(item_list.len()+1);

    if index == item_list.len()+1 {
        EventBuilder::new().string("RemoveFail").string(ipfs_hash).notify();
        return false;
    }
    item_list.swap_remove(index);

    database::put(item_key, item_list);
    EventBuilder::new().string("Remove").string(ipfs_hash).notify();
    true
}

fn clear_item_list(ont_id: &Address) -> bool {
    assert!(runtime::check_witness(ont_id));
    let item_key = [ITEM_PREFIX.as_bytes(), ont_id.as_ref()].concat();
    let item_list: Vec<Info> = database::get(&item_key).unwrap_or(Vec::<Info>::new());
    if item_list.len() == 0 {
        return false;
    }
    database::delete(item_key);
    true
}

#[no_mangle]
pub fn invoke() {
    let input = runtime::input();
    let mut source = Source::new(&input);
    let action: &str = source.read().unwrap();
    let mut sink = Sink::new(12);
    match action {
        "put_one_item" => {
            let (ont_id, encrypted_ipfs_hash, ext, aes_iv, encode_g_tilde) = source.read().unwrap();
            sink.write(put_one_item(ont_id, encrypted_ipfs_hash,ext,aes_iv,encode_g_tilde));
        }
        "get_item_list" => {
            let ont_id = source.read().unwrap();
            sink.write(get_item_list(ont_id));
        }
        "del_ont_item" => {
            let (ont_id, ipfs_hash) = source.read().unwrap();
            sink.write(del_ont_item(ont_id, ipfs_hash));
        }
        "clear_item_list" => {
            let ont_id = source.read().unwrap();
            sink.write(clear_item_list(ont_id));
        }
        _ => panic!("unsupported action!"),
    }
    runtime::ret(sink.bytes())
}

