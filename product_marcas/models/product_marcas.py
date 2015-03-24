# -*- encoding: utf-8 -*-

from openerp import models, fields, api


class Product_marcas(models.Model):
    _name = 'product.marcas'
    _rec_name = 'marca'

    def _check_unique_insesitive(self, cr, uid, ids, context=None):

        list_ids = self.search(cr, uid , [], context=context)
        lst = [list_id.marca.lower() for list_id in self.browse(cr, uid, list_ids, context=context) if list_id.marca and list_id.id not in ids]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.marca and self_obj.marca.lower() in lst:
                return False
            return True
    
    marca = fields.Char(string="Marca", required=True)
    
    _constraints = [(_check_unique_insesitive, 'La marca ya existe!', ['marca'])] 


class Product_marcas(models.Model):
    _inherit = 'product.template'

    marca = fields.Many2one('product.marcas', string="Marca", required=True)
    
    
